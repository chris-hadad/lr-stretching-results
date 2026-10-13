"""Exact trusted root mathematical functions; orchestration excluded."""
from __future__ import annotations

import argparse

from collections import Counter

from fractions import Fraction

from functools import lru_cache

import hashlib

import importlib.util

from itertools import combinations_with_replacement, product

import json

from math import comb, factorial

from pathlib import Path

import sys

import time

import traceback

ZERO = (Fraction(0),)

ONE = (Fraction(1),)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def clean(values):
    values = [Fraction(value) for value in values]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values) if values else ZERO

def add(left, right):
    size = max(len(left), len(right))
    return clean((left[i] if i < len(left) else 0)
                 + (right[i] if i < len(right) else 0) for i in range(size))

def scale(poly, value):
    return clean(coefficient * value for coefficient in poly)

def multiply(left, right):
    values = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        if first:
            for j, second in enumerate(right):
                if second:
                    values[i + j] += first * second
    return clean(values)

def evaluate(poly, grade):
    value = Fraction(0)
    for coefficient in reversed(poly):
        value = value * grade + coefficient
    return value

def degree(poly):
    return -1 if poly == ZERO else len(poly) - 1

def encode(poly, bound=None):
    values = list(poly)
    if bound is not None:
        require(degree(poly) <= bound, 'constructed polynomial exceeds prior bound')
        values += [Fraction(0)] * (bound + 1 - len(values))
    return [str(value) for value in values]

@lru_cache(maxsize=None)
def rising(index, slope=1):
    """R_index(slope*t), including its strict-first-coordinate zero case."""
    require(index >= 0 and slope >= 0, 'nonnegative rising arguments required')
    poly = ONE
    for shift in range(index):
        poly = multiply(poly, (Fraction(shift), Fraction(slope)))
    return scale(poly, Fraction(1, factorial(index)))

@lru_cache(maxsize=None)
def weak_chain(nodes):
    return rising(nodes)

@lru_cache(maxsize=None)
def strict_junction(nodes):
    """E_nodes(t), used only inside complete one-node factors or controls."""
    require(nodes >= 1, 'positive node count required')
    poly = ONE
    for shift in range(-1, nodes - 1):
        poly = multiply(poly, (Fraction(shift), Fraction(1)))
    return scale(poly, Fraction(1, factorial(nodes)))

@lru_cache(maxsize=None)
def attached_chain(nodes, position, relation):
    require(nodes >= 1 and 1 <= position <= nodes, 'invalid surviving q node')
    require(relation in ('below', 'above'), 'unknown singleton relation')
    extra_slots = position - 1 if relation == 'below' else nodes - position
    # Preserve the complete factor. E alone is not a positivity premise.
    return add(weak_chain(nodes + 1),
               scale(strict_junction(nodes + 1), extra_slots))

def A(index, value):
    return comb(value + index, index)

def R(index, value):
    if index == 0:
        return 1
    return 0 if value == 0 else comb(value + index - 1, index)

class CeilingExceeded(RuntimeError):
    pass

class Budget:
    def __init__(self, limit, label):
        self.limit, self.label, self.used = limit, label, 0

    def step(self):
        self.used += 1
        if self.used > self.limit:
            raise CeilingExceeded(f'{self.label} ceiling {self.limit} exceeded')

def direct_F(fixture, grade, limit):
    """Separate literal scalar sum; does not use chain cells."""
    r, n, delta, lower, upper = (fixture[key] for key in ('r', 'n', 'delta', 'V', 'U'))
    budget = Budget(limit, 'direct F summands')
    total = 0
    for x in range(delta * grade + 1):
        for y in range(max(0, lower * grade - x), upper * grade - x + 1):
            budget.step()
            total += R(r, x) * A(n, y)
    return total, budget.used

def direct_J(fixture, grade, limit):
    """Separate literal three-variable scalar sum; no q/chain transform."""
    n, m, delta, height, lower, upper = (
        fixture[key] for key in ('n', 'm', 'delta', 'H', 'V', 'U'))
    budget = Budget(limit, 'direct J summands')
    total = 0
    for x in range(delta * grade + 1):
        for w in range(height * grade + 1):
            for z in range(max(0, lower * grade - x - w),
                           upper * grade - x - w + 1):
                budget.step()
                total += A(n, x + w) * A(m, z)
    return total, budget.used

def positive_blocks(beta, fixed_last):
    """Original half-open node intervals and their actual free lengths."""
    result = []
    start = 0
    while start < len(beta):
        stop = start + 1
        while stop < len(beta) and beta[stop] == beta[start]:
            stop += 1
        if beta[start] > 0:
            removed = int(fixed_last and stop == len(beta))
            result.append(dict(beta=beta[start], start=start, stop=stop,
                               original_nodes=stop - start,
                               free_nodes=stop - start - removed,
                               removed_last_node=bool(removed)))
        start = stop
    return result

def flag_status(beta, lower):
    if lower > 0 and beta[-1] < lower:
        return 'lower_flag_excluded'
    if lower > 0 and beta[-1] == lower:
        return 'fixed_last'
    return 'free_last'

def emit_cell(writer, name, row):
    if writer is not None:
        writer(dict(fixture=name, **row))

def cell_F(fixture, caps, writer=None, *, bad_fixed_last=False):
    r, n, delta, lower, upper = (fixture[key] for key in ('r', 'n', 'delta', 'V', 'U'))
    nodes = r + n + 2 if r > 0 else n + 2
    flag_index = r if r > 0 else 0  # Zero-based X_(r+1), or X_1.
    first_beta = 1 if r > 0 else 0
    budget = Budget(caps['cell_states_per_fixture'], 'F cell states')
    coverage = Counter()
    answer = ZERO
    for beta in combinations_with_replacement(range(first_beta, upper + 1), nodes):
        budget.step()
        coverage['candidate_cells'] += 1
        status = flag_status(beta, lower)
        if beta[flag_index] > delta:
            status = 'internal_flag_excluded'
        if status.endswith('_excluded'):
            coverage[status] += 1
            emit_cell(writer, fixture['id'], dict(beta=list(beta), admitted=False,
                                                 reason=status))
            continue
        fixed = status == 'fixed_last'
        blocks = positive_blocks(beta, fixed)
        poly = ONE
        for block in blocks:
            count = block['free_nodes']
            if bad_fixed_last and block['removed_last_node']:
                count = 0  # Deliberately wrong: delete the entire final block.
            poly = multiply(poly, weak_chain(count))
        coverage['admitted_cells'] += 1
        coverage[status] += 1
        if beta[0] == 0:
            coverage['zero_prefix'] += 1
        if not blocks:
            coverage['all_fixed_zero'] += 1
        if any(block['original_nodes'] > 1 for block in blocks):
            coverage['positive_chain_tie'] += 1
        answer = add(answer, poly)
        emit_cell(writer, fixture['id'], dict(beta=list(beta), admitted=True,
                    final_flag=status, blocks=blocks, coefficients=encode(poly)))
    return answer, dict(coverage), nodes

def cell_J(fixture, caps, writer=None):
    n, m, delta, height, lower, upper = (
        fixture[key] for key in ('n', 'm', 'delta', 'H', 'V', 'U'))
    nodes, q_index = n + m + 2, n
    budget = Budget(caps['cell_states_per_fixture'], 'J cell states')
    coverage = Counter()
    answer = ZERO
    for beta in combinations_with_replacement(range(upper + 1), nodes):
        status = flag_status(beta, lower)
        for extra_beta in range(min(delta, upper) + 1):
            budget.step()
            coverage['candidate_cells'] += 1
            row = dict(beta=list(beta), extra_beta=extra_beta)
            q_beta = beta[q_index]
            reason = status if status.endswith('_excluded') else None
            relation = None
            if extra_beta == 0:
                relation = 'fixed_zero'
                if q_beta > height:
                    reason = reason or 'zero_extra_cap_excluded'
            elif extra_beta > q_beta or q_beta - extra_beta > height:
                reason = reason or 'extra_cap_excluded'
            elif height == 0:
                relation = 'identified_with_q'
            elif extra_beta == q_beta:
                relation = 'below'
            elif q_beta - extra_beta == height:
                relation = 'above'
            else:
                relation = 'independent'
            if reason is not None:
                coverage[reason] += 1
                emit_cell(writer, fixture['id'], dict(**row, admitted=False, reason=reason))
                continue
            fixed = status == 'fixed_last'
            blocks = positive_blocks(beta, fixed)
            poly = ONE
            q_position = None
            q_free_nodes = None
            for block in blocks:
                count = block['free_nodes']
                is_q_block = block['start'] <= q_index < block['stop']
                if is_q_block:
                    q_position = q_index - block['start'] + 1
                    q_free_nodes = count
                    require(q_position <= count, 'fixed final node incorrectly removed q')
                if is_q_block and relation in ('below', 'above'):
                    factor = attached_chain(count, q_position, relation)
                else:
                    factor = weak_chain(count)
                poly = multiply(poly, factor)
            if relation == 'independent':
                poly = multiply(poly, (Fraction(0), Fraction(1)))
            coverage['admitted_cells'] += 1
            coverage[relation] += 1
            coverage[status] += 1
            if beta[0] == 0:
                coverage['zero_prefix'] += 1
            if any(block['original_nodes'] > 1 for block in blocks):
                coverage['positive_chain_tie'] += 1
            matches_other_block = (relation == 'above' and extra_beta in beta
                                   and extra_beta != q_beta)
            if matches_other_block:
                coverage['above_extra_beta_matches_other_block'] += 1
            if fixed and q_beta > 0:
                coverage['fixed_last_q_survives'] += 1
            answer = add(answer, poly)
            emit_cell(writer, fixture['id'], dict(**row, admitted=True,
                        final_flag=status, relation=relation, blocks=blocks,
                        q_index=q_index, q_position=q_position,
                        q_free_nodes=q_free_nodes,
                        extra_beta_matches_other_block=matches_other_block,
                        coefficients=encode(poly)))
    return answer, dict(coverage), nodes + 1

def validate_fixture(row):
    family = row.get('family')
    require(family in ('F', 'J'), 'unknown auxiliary family')
    keys = ('r', 'n', 'delta', 'V', 'U') if family == 'F' else ('n', 'm', 'delta', 'H', 'V', 'U')
    require(all(type(row[key]) is int and row[key] >= 0 for key in keys),
            'exact nonnegative fixture parameters required')
    require(row['V'] <= row['U'], 'reversed final band')

def fixture_id(family, **parameters):
    order = ('r', 'n', 'delta', 'V', 'U') if family == 'F' else ('n', 'm', 'delta', 'H', 'V', 'U')
    return family + '-' + '-'.join(f'{key}{parameters[key]}' for key in order)

def expected_domain():
    rows = []
    for r, n, delta in product(range(5), range(4), range(3)):
        for upper in range(3):
            for lower in range(upper + 1):
                args = dict(r=r, n=n, delta=delta, V=lower, U=upper)
                rows.append(dict(id=fixture_id('F', **args), family='F', **args))
    for n, m, delta, height in product(range(4), range(4), range(3), range(3)):
        for upper in range(3):
            for lower in range(upper + 1):
                args = dict(n=n, m=m, delta=delta, H=height, V=lower, U=upper)
                rows.append(dict(id=fixture_id('J', **args), family='J', **args))
    return rows
