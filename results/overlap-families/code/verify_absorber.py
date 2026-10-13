"""Independent exact audit of the Pro048 U01 two-cap absorber certificate.

The mathematical constructions here come from the proof definitions.  No
returned scientific program is imported or executed.  The accepted A58 bare
original counter is imported only in the explicit price/original modes.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations_with_replacement
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def frac_vector(values):
    return tuple(F(x) for x in values)


def product(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return tuple(out)


def polynomial_value(poly, t):
    return sum(coefficient * t**j for j, coefficient in enumerate(poly))


def monomial_from_values(values, n):
    """Newton forward differences, using only grades 0 through n."""
    differences = []
    row = list(values[:n + 1])
    for j in range(n + 1):
        differences.append(row[0])
        row = [b - a for a, b in zip(row, row[1:])]
    poly = [F(0)] * (n + 1)
    choose = [F(1)]
    for j, coefficient in enumerate(differences):
        for k, basis_coefficient in enumerate(choose):
            poly[k] += coefficient * basis_coefficient
        if j < n:
            following = [F(0)] * (len(choose) + 1)
            for k, basis_coefficient in enumerate(choose):
                following[k] -= F(j, j + 1) * basis_coefficient
                following[k + 1] += basis_coefficient / (j + 1)
            choose = following
    return tuple(poly), tuple(differences)


def poset_predecessors(levels, active):
    """Closure of equal-band chains and reversed active interval comparisons."""
    z = 0
    while z < len(levels) and levels[z] == 0:
        z += 1
    require(all(x > 0 for x in levels[z:]), 'non-prefix zero levels')
    n = len(levels) - z
    outgoing = [0] * n
    for i in range(z, len(levels) - 1):
        if levels[i] == levels[i + 1]:
            outgoing[i - z] |= 1 << (i + 1 - z)
    for edge in active:
        left, right = edge[:2]
        require(0 < left < right <= len(levels), 'invalid active row endpoints')
        require(0 < levels[left - 1] < levels[right - 1], 'inactive row listed active')
        outgoing[right - 1 - z] |= 1 << (left - 1 - z)
    reach = outgoing[:]
    for middle in range(n):
        for i in range(n):
            if reach[i] & (1 << middle):
                reach[i] |= reach[middle]
    require(all(not (reach[i] & (1 << i)) for i in range(n)), 'comparison cycle')
    pred = [0] * n
    for i, following in enumerate(reach):
        for j in range(n):
            if following & (1 << j):
                pred[j] |= 1 << i
    return tuple(pred)


_POLYNOMIALS = {}


def order_polynomial(pred):
    """Count maps to [t] by subset-zeta over order ideals through n+2.

    The strict ideal-layer identity bounds degree by n.  The final two values
    are checked after interpolation and never used to determine coefficients.
    """
    pred = tuple(pred)
    if pred in _POLYNOMIALS:
        return _POLYNOMIALS[pred]
    n = len(pred)
    size = 1 << n
    ideals = [all(not mask & (1 << i) or pred[i] & mask == pred[i]
                  for i in range(n)) for mask in range(size)]
    old = [0] * size
    old[0] = 1
    values = [old[-1]]
    for _ in range(n + 2):
        zeta = old[:]
        for bit in range(n):
            for mask in range(size):
                if mask & (1 << bit):
                    zeta[mask] += zeta[mask ^ (1 << bit)]
        old = [zeta[mask] if ideals[mask] else 0 for mask in range(size)]
        values.append(old[-1])
    poly, layers = monomial_from_values(values, n)
    for t in (n + 1, n + 2):
        require(polynomial_value(poly, t) == values[t], 'unused-grade poset holdout')
    require(all(x >= 0 for x in layers), 'negative strict ideal-layer count')
    _POLYNOMIALS[pred] = (poly, layers, tuple(values))
    return _POLYNOMIALS[pred]


def compositions(n):
    if n == 0:
        yield ()
        return
    for cuts in range(1 << (n - 1)):
        lengths = []
        last = 0
        for i in range(n - 1):
            if cuts & (1 << i):
                lengths.append(i + 1 - last)
                last = i + 1
        lengths.append(n - last)
        yield tuple(lengths)


def normalized_levels(n):
    for z in range(n + 1):
        for lengths in compositions(n - z):
            result = [0] * z
            for band, length in enumerate(lengths, 1):
                result.extend([band] * length)
            yield tuple(result)


def quotient(mask):
    """Primitive equalities among x_0,...,x_9, including x_0=0."""
    p, delta, kappa, eta = mask
    parent = list(range(10))

    def root(i):
        while parent[i] != i:
            i = parent[i]
        return i

    def collapse(left, right):
        for i in range(left, right):
            parent[root(i + 1)] = root(i)

    if not p:
        collapse(1, 6)
    if not delta:
        collapse(4, 5)
    if not eta:
        collapse(5, 7)
    if not kappa:
        collapse(0, 2)
    indices = {}
    mapping = []
    for i in range(10):
        representative = root(i)
        if representative not in indices:
            indices[representative] = len(indices)
        mapping.append(indices[representative])
    n = max(mapping)
    rows = []
    for positive, left, right in ((p, 1, 6), (delta, 4, 5), (eta, 5, 7)):
        if positive and mapping[left] < mapping[right]:
            rows.append((mapping[left], mapping[right], len(rows)))
    flags = [(mapping[2], 1)] if kappa and mapping[2] else []
    return n, tuple(mapping), tuple(rows), tuple(flags)


def type_key(levels, active):
    return tuple(levels), tuple(tuple(edge) for edge in active)


def all_types(mask):
    n, mapping, rows, flags = quotient(mask)
    result = {}
    for levels in normalized_levels(n):
        eligible = []
        for left, right, index in rows:
            left_band = levels[left - 1] if left else 0
            right_band = levels[right - 1]
            if 0 < left_band < right_band:
                eligible.append((left, right, index))
        for subset in range(1 << len(eligible)):
            active = tuple(edge for j, edge in enumerate(eligible)
                           if subset & (1 << j))
            key = type_key(levels, active if mask != (1, 1, 1, 1)
                           else tuple(edge[:2] for edge in active))
            pred = poset_predecessors(levels, active)
            require(key not in result, 'duplicate generated type')
            result[key] = (pred, order_polynomial(pred)[0])
    return result, (n, mapping, rows, flags)


def determinant(matrix):
    n = len(matrix)
    require(all(len(row) == n for row in matrix), 'nonsquare minor')
    if n == 0:
        return F(1)
    a = [[F(x) for x in row] for row in matrix]
    sign = 1
    result = F(1)
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign = -sign
        value = a[col][col]
        result *= value
        for i in range(col + 1, n):
            ratio = a[i][col] / value
            for j in range(col, n):
                a[i][j] -= ratio * a[col][j]
    return sign * result


def contraction(levels, active, gaps):
    gaps = tuple(gaps)
    require(gaps and len(gaps) == len(set(gaps)), 'repeated or empty removed gap')
    require(all(1 <= g < max(levels) for g in gaps), 'gap out of range')
    incidence = tuple(tuple(int(levels[left - 1] <= gap < levels[right - 1])
                            for gap in gaps) for left, right, *_ in active)
    new_levels = tuple(level - sum(g < level for g in gaps) if level else 0
                       for level in levels)
    new_active = tuple(edge for edge, row in zip(active, incidence)
                       if not any(row))
    return new_levels, new_active, incidence


def check_minor(incidence, rows, displayed):
    require(len(rows) == (len(incidence[0]) if incidence else 0),
            'rank-deficient recovery: wrong minor size')
    require(len(set(rows)) == len(rows), 'rank-deficient recovery: repeated minor row')
    require(all(0 <= i < len(incidence) for i in rows), 'minor row out of range')
    value = determinant([incidence[i] for i in rows])
    require(abs(value) == 1 and value == F(displayed),
            'rank-deficient recovery or wrong unit minor')
    return value


def nonunit_inverse_control(levels, active, full_rows, gaps, minor_rows):
    """Construct a realizable nonunit-gap state and recover every removed gap.

    For the three positive-width rows (or the two surviving boundary rows),
    set active widths to exact source differences and inactive widths one
    larger.  Larger d and flags admit the state, and the contracted state must
    retain the same width choices.  Cramer's rule then tests the inverse.
    """
    gaps = tuple(gaps)
    gap_sizes = {h: h + 1 for h in range(1, max(levels))}
    source = tuple(0 if level == 0 else
                   2 + sum(gap_sizes[h] for h in range(1, level))
                   for level in levels)
    target = tuple(value - sum(gap_sizes[h] for h in gaps if h < level)
                   for value, level in zip(source, levels))
    target_levels, target_active, incidence = contraction(levels, active, gaps)
    require(all(a <= b for a, b in zip(source, source[1:])) and
            all(a <= b for a, b in zip(target, target[1:])),
            'nonunit contraction broke band order')
    active_pairs = {tuple(edge[:2]) for edge in active}
    target_pairs = {tuple(edge[:2]) for edge in target_active}
    for left, right, *_ in full_rows:
        pair = (left, right)
        source_difference = source[right - 1] - (source[left - 1] if left else 0)
        target_difference = target[right - 1] - (target[left - 1] if left else 0)
        width = source_difference + (pair not in active_pairs)
        require(width > 0 and target_difference <= source_difference <= width,
                'nonunit width admission')
        require((source[left - 1] > 0 and source_difference == width) ==
                (pair in active_pairs), 'nonunit source active row')
        require((target[left - 1] > 0 and target_difference == width) ==
                (pair in target_pairs), 'nonunit target active row')
    matrix = [incidence[i] for i in minor_rows]
    determinant_value = determinant(matrix)
    require(abs(determinant_value) == 1, 'nonunit recovery rank')
    right_hand = []
    for i in minor_rows:
        left, right = active[i][:2]
        width = source[right - 1] - source[left - 1]
        right_hand.append(width - (target[right - 1] - target[left - 1]))
    recovered = []
    for column in range(len(gaps)):
        replaced = [list(row) for row in matrix]
        for i, value in enumerate(right_hand):
            replaced[i][column] = value
        recovered.append(determinant(replaced) / determinant_value)
    require(tuple(recovered) == tuple(gap_sizes[h] for h in gaps),
            'nonunit removed-gap recovery')
    reconstruction = tuple(value + sum(recovered[j] for j, h in enumerate(gaps)
                                       if h < level)
                           for value, level in zip(target, levels))
    require(reconstruction == source, 'nonunit source reconstruction')
    return True


def mask_from_case(case):
    return tuple(case['positive_mask_p_delta_k_l'])


def check_classes(factor_data, boundary_data):
    expected = {}
    descriptions = {}
    for bits in range(16):
        mask = tuple((bits >> shift) & 1 for shift in (3, 2, 1, 0))
        generated, description = all_types(mask)
        expected[mask] = generated
        descriptions[mask] = description
    require(sum(len(x) for x in expected.values()) == 3520,
            'complete normalized type count')
    class_posets = len(_POLYNOMIALS)
    require(class_posets == 2340, 'distinct complete-type poset count')
    positive = expected[(1, 1, 1, 1)]
    require(len(positive) == 1964, 'positive type count')
    roster = factor_data['type_roster']
    require(len(roster) == len(positive), 'source positive roster size')
    source_keys = set()
    for record in roster:
        key = type_key(record['levels'], record['active_edges'])
        require(key in positive and key not in source_keys,
                'positive source key missing or duplicated')
        source_keys.add(key)
        pred, poly = positive[key]
        require(tuple(record['pred']) == pred, 'positive source predecessor mismatch')
        factors = [frac_vector(factor_data['connected_factors'][i]['coefficients'])
                   for i in record['factors']]
        source_poly = (F(1),)
        for factor in factors:
            source_poly = product(source_poly, factor)
        require(source_poly == poly, 'positive source complete polynomial mismatch')
    require(source_keys == set(positive), 'positive full type-set mismatch')
    require(len({v[0] for v in positive.values()}) == 1952,
            'positive labeled poset count')
    require(len(factor_data['connected_factors']) == 284,
            'source connected factor count')
    for item in factor_data['connected_factors']:
        poly, layers, _ = order_polynomial(item['pred'])
        require(frac_vector(item['coefficients']) == poly,
                'connected factor polynomial mismatch')
        require(tuple(item['strict_ideal_chains']) == layers,
                'connected factor ideal chains mismatch')
    boundary_cases = {mask_from_case(case): case for case in boundary_data['cases']}
    require(len(boundary_cases) == 15 and (1, 1, 1, 1) not in boundary_cases,
            'boundary case roster')
    counts = []
    for mask, generated in expected.items():
        bad_keys = {key for key, (_, poly) in generated.items()
                    if any(x < 0 for x in poly)}
        if mask == (1, 1, 1, 1):
            require(len(bad_keys) == 31, 'positive negative-type count')
            require(all(key[0][0] > 0 and (1, 6) in key[1]
                        for key in bad_keys), 'unexpected positive negative-type shape')
        else:
            source = boundary_cases[mask]
            n, mapping, rows, flags = descriptions[mask]
            require(source['dimension'] == n, 'primitive quotient dimension')
            require({int(k): v for k, v in source['mapping'].items()} ==
                    dict(enumerate(mapping)), 'primitive quotient map')
            require(tuple(tuple(x) for x in source['collapsed_spans']) ==
                    tuple((left, right, 1) for left, right, _ in rows),
                    'surviving quotient interval rows')
            require(tuple(tuple(x) for x in source['collapsed_flags']) == flags,
                    'surviving quotient flags')
            require(n == (3 + mask[2] + mask[3] - 1 if not mask[0]
                          else 2 * (3 + mask[2] + mask[3]) - 1 - (not mask[1])),
                    'degree formula vs primitive dimension')
            require(source['type_count'] == len(generated) and
                    len(source['types']) == len(generated), 'boundary type count')
            found = set()
            for record in source['types']:
                key = type_key(record['levels'], record['active'])
                require(key in generated and key not in found,
                        'boundary source key missing or duplicated')
                found.add(key)
                pred, poly = generated[key]
                require(tuple(record['pred']) == pred and
                        frac_vector(record['poly']) == poly,
                        'boundary complete polynomial mismatch')
            require(found == set(generated), 'boundary full type-set mismatch')
            source_bad = {type_key(x['levels'], x['active'])
                          for x in source['negative_types']}
            require(source_bad == bad_keys and
                    source['negative_type_count'] == len(bad_keys),
                    'boundary bad-type roster mismatch')
        counts.append({'mask': ''.join(map(str, mask)),
                       'dimension': descriptions[mask][0],
                       'types': len(generated), 'bad': len(bad_keys)})
    return expected, descriptions, counts, class_posets


def source_bad_key(record):
    return type_key(record['levels'], record.get('active_edges', record.get('active')))


def check_positive_payment(data, positive):
    certificate = data['certificate']
    bad = certificate['bad_types']
    actual_bad = {key for key, (_, poly) in positive.items()
                  if any(x < 0 for x in poly)}
    require(len(bad) == 31 and {source_bad_key(x) for x in bad} == actual_bad,
            'missing or duplicate positive bad type')
    for i, record in enumerate(bad):
        require(record['id'] == i, 'bad ID sequence')
        key = source_bad_key(record)
        poly = positive[key][1]
        require(frac_vector(record['poly']) == poly, 'bad source polynomial')
        require(frac_vector(record['loss']) == tuple(max(-x, 0) for x in poly),
                'bad source negative part')
    require(len(data['all_targets']) == 84 and len(data['all_edges']) == 146,
            'complete candidate target or edge population')
    targets = {x['id']: x for x in data['all_targets']}
    edges = {x['id']: x for x in data['all_edges']}
    require(len(targets) == 84 and len(edges) == 146,
            'candidate target or edge IDs duplicated')
    for target in targets.values():
        key = source_bad_key(target)
        require(key in positive, 'candidate target absent from complete type set')
        pred, poly = positive[key]
        require(tuple(target['pred']) == pred and
                frac_vector(target['poly']) == poly and all(x >= 0 for x in poly),
                'candidate target polynomial or positivity')
    for edge in edges.values():
        require(0 <= edge['bad_id'] < len(bad) and edge['target_id'] in targets,
                'candidate edge endpoint')
        source = bad[edge['bad_id']]
        levels, active, incidence = contraction(
            source['levels'], source['active_edges'], edge['removed_gap_labels'])
        require(tuple(map(tuple, edge['active_incidence'])) == incidence,
                'candidate edge active incidence')
        check_minor(incidence, edge['independent_rows'], edge['pivot_determinant'])
        nonunit_inverse_control(source['levels'], source['active_edges'],
                                ((1, 6), (4, 5), (5, 7)),
                                edge['removed_gap_labels'],
                                edge['independent_rows'])
        require(type_key(levels, active) == source_bad_key(targets[edge['target_id']]),
                'candidate contraction target type')
    groups = certificate['groups']
    require(len(groups) == 30, 'used target group count')
    seen_edges = set()
    seen_targets = set()
    outgoing = defaultdict(F)
    minimum = F(1)
    for group in groups:
        target = group['target']
        target_id = target['id']
        require(target_id in targets and target_id not in seen_targets and
                target == targets[target_id], 'group target mismatch or duplicate')
        seen_targets.add(target_id)
        omega = positive[source_bad_key(target)][1]
        negative_debt = [F(0)] * len(omega)
        whole_reserve = list(omega)
        for weighted in group['incoming']:
            edge_id = weighted['id']
            require(edge_id in edges and edge_id not in seen_edges and
                    {k: v for k, v in weighted.items() if k != 'weight'} ==
                    edges[edge_id] and weighted['target_id'] == target_id,
                    'group edge mismatch or duplicate')
            seen_edges.add(edge_id)
            require(any(edges[edge_id]['active_incidence'][0]),
                    'used contraction does not cross long budget row')
            weight = F(weighted['weight'])
            require(weight > 0 and weight.denominator <= 420,
                    'invalid rational edge weight')
            source = bad[weighted['bad_id']]
            outgoing[weighted['bad_id']] += weight
            source_poly = positive[source_bad_key(source)][1]
            for j, value in enumerate(source_poly):
                negative_debt[j] += weight * max(-value, 0)
                whole_reserve[j] += weight * value
        reserve = tuple(x - y for x, y in zip(omega, negative_debt))
        require(frac_vector(group['negative_part_reserve']) == reserve,
                'group exact negative-part reserve mismatch')
        require(frac_vector(group['whole_poly_reserve']) == tuple(whole_reserve),
                'group whole-source reserve mismatch')
        for base, retained in zip(omega, reserve):
            require(retained >= F(121, 140) * base,
                    'positive group retained ratio below 121/140')
            if base:
                minimum = min(minimum, retained / base)
    require(len(seen_edges) == 48 and len(seen_targets) == 30,
            'positive rational edge or target count')
    require(set(outgoing) == set(range(31)) and
            all(value == 1 for value in outgoing.values()),
            'bad-source outgoing rational sum not one')
    require(minimum == F(121, 140), 'exact positive minimum retained ratio')
    return {'bad_types': 31, 'candidate_edges': len(edges),
            'candidate_targets': len(targets), 'weighted_edges': len(seen_edges),
            'used_targets': len(seen_targets), 'minimum_retained': str(minimum),
            'nonunit_inverse_controls': len(edges)}


def check_boundary_payment(data, expected):
    require(len(data['cases']) == 2, 'boundary payment case count')
    summary = []
    global_minimum = F(1)
    seen_masks = set()
    for case in data['cases']:
        mask = mask_from_case(case)
        require(mask in ((1, 0, 1, 1), (1, 1, 1, 0)) and
                mask not in seen_masks, 'boundary payment mask')
        seen_masks.add(mask)
        generated = expected[mask]
        actual_bad = {key for key, (_, poly) in generated.items()
                      if any(x < 0 for x in poly)}
        bad = case['bad_types']
        require(len(bad) == (3 if mask == (1, 0, 1, 1) else 7) and
                {source_bad_key(x['source']) for x in bad} == actual_bad,
                'boundary missing bad type')
        by_id = {}
        contracted = {}
        for record in bad:
            source = record['source']
            identifier = record['id']
            require(identifier not in by_id and F(record['weight']) == 1,
                    'boundary bad ID or weight')
            by_id[identifier] = record
            key = source_bad_key(source)
            pred, poly = generated[key]
            require(tuple(source['pred']) == pred and
                    frac_vector(source['poly']) == poly,
                    'boundary source polynomial')
            levels, active, incidence = contraction(
                source['levels'], source['active'], record['removed_gap_labels'])
            require(tuple(map(tuple, record['active_incidence'])) == incidence,
                    'boundary incidence mismatch')
            require(incidence == ((1, 1), (0, 1)) and
                    determinant(incidence) == F(record['pivot_determinant']) == 1,
                    'boundary rank-deficient recovery')
            nonunit_inverse_control(source['levels'], source['active'],
                                    tuple((x[0], x[1]) for x in source['active']),
                                    record['removed_gap_labels'], (0, 1))
            require(not active, 'boundary target active edge remains')
            contracted[identifier] = type_key(levels, active)
        require(set(by_id) == set(range(len(bad))), 'boundary bad ID sequence')
        groups = case['groups']
        require(len(groups) == (3 if mask == (1, 0, 1, 1) else 5),
                'boundary grouped target count')
        used = set()
        group_keys = set()
        minimum = F(1)
        for group in groups:
            key = type_key(group['target_levels'], group['target_edges'])
            require(key in generated and key not in group_keys,
                    'boundary target missing or duplicate')
            group_keys.add(key)
            pred, omega = generated[key]
            require(tuple(group['target_pred']) == pred and
                    frac_vector(group['target_poly']) == omega and
                    all(x >= 0 for x in omega),
                    'boundary target complete polynomial')
            loss = [F(0)] * len(omega)
            for identifier in group['bad_ids']:
                require(identifier in by_id and identifier not in used and
                        contracted[identifier] == key,
                        'boundary contraction target or duplicate source')
                used.add(identifier)
                source_poly = generated[source_bad_key(by_id[identifier]['source'])][1]
                for j, value in enumerate(source_poly):
                    loss[j] += max(-value, 0)
            reserve = tuple(x - y for x, y in zip(omega, loss))
            require(frac_vector(group['reserve']) == reserve,
                    'boundary exact reserve mismatch')
            for base, retained in zip(omega, reserve):
                require(retained >= F(7, 10) * base,
                        'boundary retained ratio below 7/10')
                if base:
                    minimum = min(minimum, retained / base)
        require(used == set(by_id), 'boundary bad type not paid')
        global_minimum = min(global_minimum, minimum)
        summary.append({'mask': ''.join(map(str, mask)), 'bad_types': len(bad),
                        'targets': len(groups), 'minimum_retained': str(minimum),
                        'nonunit_inverse_controls': len(bad)})
    require(global_minimum == F(7, 10), 'exact boundary minimum retained ratio')
    return summary


def literal_original(caps, b, c, h, u, v):
    k = tuple(caps)
    total = sum(k)
    sigma = [sum(k[i:]) for i in range(5)]
    outer = (total + u + v - h, total + v, sigma[0], sigma[1],
             sigma[2], sigma[3], sigma[4])
    inner = (total + v - h, total, sigma[1], sigma[2], sigma[3],
             sigma[4], 0)
    content = (u + v + total - b - c, b, c)
    require(sum(outer) == sum(inner) + sum(content), 'literal size balance')
    return outer, inner, content


def pair_original(pair):
    kappa, eta = (int(x) for x in pair)
    caps = (kappa, eta, 3, 3, 3)
    total = sum(caps)
    c = total - 3
    b = c + 1
    return literal_original(caps, b, c, b - 2, b, b), caps, (3, 2, 1, kappa, eta)


def mask_original(mask):
    p, delta, kappa, eta = mask
    caps = (kappa, eta, 1, 1, 1)
    total = sum(caps)
    c = total - 1
    b = c + delta
    return literal_original(caps, b, c, b - p, b, b), caps, (1, p, delta, kappa, eta)


def residual_count(t, d, p, delta, caps, *, offset=0):
    """Direct pair DP for (6), with an optional wrong once-only shift.

    Correct offset zero means U_5 <= delta*t.  Offsets -1 and +1 model
    omitting or doubling the affine +1 in the second partner's injection.
    """
    total = d * t
    budget = p * t
    absorber_bound = delta * t + offset
    if absorber_bound < 0:
        return 0
    states = {(0, 0): 1}
    for i, cap in enumerate(caps):
        nxt = defaultdict(int)
        pair_limit = min(total, cap * t)
        for (old_total, old_u), multiplicity in states.items():
            for pair_total in range(min(pair_limit, total - old_total) + 1):
                for u in range(pair_total + 1):
                    if old_u + u > budget or (i == 4 and u > absorber_bound):
                        continue
                    nxt[(old_total + pair_total, old_u + u)] += multiplicity
        states = nxt
    return sum(value for (used_total, _), value in states.items()
               if used_total == total)


def actual_band_polynomial(d, p, delta, kappa, eta):
    mask = tuple(int(x > 0) for x in (p, delta, kappa, eta))
    n, mapping, rows, flags = quotient(mask)
    result = [F(0)] * (n + 1)
    band_count = 0
    row_widths = []
    for width, left, right in ((p, 1, 6), (delta, 4, 5), (eta, 5, 7)):
        if width > 0 and mapping[left] < mapping[right]:
            row_widths.append(width)
    require(len(rows) == len(row_widths), 'surviving interval-width order')
    for levels in combinations_with_replacement(range(d + 1), n):
        if any(levels[index - 1] > kappa for index, _ in flags):
            continue
        active = []
        valid = True
        for (left, right, index), width in zip(rows, row_widths):
            left_band = levels[left - 1] if left else 0
            difference = levels[right - 1] - left_band
            if difference > width:
                valid = False
                break
            if left_band and difference == width:
                active.append((left, right, index))
        if not valid:
            continue
        pred = poset_predecessors(levels, active)
        poly = order_polynomial(pred)[0]
        for j, value in enumerate(poly):
            result[j] += value
        band_count += 1
    return tuple(result), band_count


def import_original_counter(path):
    spec = importlib.util.spec_from_file_location('accepted_a58_original_count', path)
    require(spec is not None and spec.loader is not None, 'A58 counter import spec')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def count_original(module, original, t):
    statistics = {}
    value = module.stretched_lr_count(*original, t, statistics=statistics,
                                      max_states=2_000_000)
    return value, statistics


def check_originals(bare_records, original_counter):
    result = []
    for pair in ('11', '12', '22'):
        original, caps, parameters = pair_original(pair)
        record = bare_records[pair]
        require(record['id'] == 'A-pair-' + pair and
                tuple(record['original']['outer']) == original[0] and
                tuple(record['original']['inner']) == original[1] and
                tuple(record['original']['content']) == original[2],
                'literal rank-seven original mismatch')
        d, p, delta, kappa, eta = parameters
        poly, actual_bands = actual_band_polynomial(d, p, delta, kappa, eta)
        require(len(poly) == 10 and poly[-1] > 0 and
                all(value > 0 for value in poly), 'actual degree-nine positivity')
        require(frac_vector(record['coefficients']) == poly,
                'source original complete coefficient vector')
        source_rows = {row['t']: row['value'] for row in record['rows']}
        observed_rows = []
        for t in range(12):
            tableau, stats = count_original(original_counter, original, t)
            residual = residual_count(t, d, p, delta, caps)
            expected = polynomial_value(poly, t)
            require(tableau == residual == expected == source_rows[t],
                    f'original, residual and band count at {pair}, t={t}')
            observed_rows.append({'t': t, 'value': tableau,
                                  'states': stats['states']})
        wrong_at_two = {
            'omitted_shift': residual_count(2, d, p, delta, caps, offset=-1),
            'doubled_shift': residual_count(2, d, p, delta, caps, offset=1),
        }
        require(wrong_at_two['omitted_shift'] != source_rows[2] and
                wrong_at_two['doubled_shift'] != source_rows[2],
                'once-only affine shift negative control')
        rejected_offsets = []
        for label, offset in (('omitted once-only shift', -1),
                              ('doubled once-only shift', 1)):
            expect_mutation_rejected(
                label, offset,
                lambda x: require(residual_count(2, d, p, delta, caps,
                                                 offset=x) == source_rows[2],
                                  'wrong affine offset changes whole original'),
                rejected_offsets)
        result.append({'pair': pair, 'degree': 9, 'bands': actual_bands,
                       'determining_grades': list(range(10)),
                       'unused_holdouts': [10, 11], 'tableau_rows': observed_rows,
                       'wrong_shift_t2': wrong_at_two,
                       'offset_mutations_rejected': rejected_offsets})
    return result


def check_zero_controls(original_counter):
    controls = []
    for bits in range(16):
        mask = tuple((bits >> shift) & 1 for shift in (3, 2, 1, 0))
        original, caps, (d, p, delta, kappa, eta) = mask_original(mask)
        poly, bands = actual_band_polynomial(d, p, delta, kappa, eta)
        expected_degree = quotient(mask)[0]
        require(len(poly) == expected_degree + 1 and poly[-1] > 0,
                'zero-mask actual degree')
        grades = []
        for t in (1, 2):
            tableau, stats = count_original(original_counter, original, t)
            residual = residual_count(t, d, p, delta, caps)
            require(tableau == residual == polynomial_value(poly, t),
                    f'zero-mask original/residual/band control {mask}, t={t}')
            grades.append({'t': t, 'value': tableau, 'states': stats['states']})
        controls.append({'mask': ''.join(map(str, mask)),
                         'degree': expected_degree, 'bands': bands,
                         'grade_controls': grades})
    # K=c, so the residual total is zero and the family is a point.
    caps = (0, 0, 0, 0, 1)
    point = literal_original(caps, 1, 1, 1, 1, 1)
    for t in (0, 1, 2, 3):
        tableau, _ = count_original(original_counter, point, t)
        require(tableau == residual_count(t, 0, 0, 0, caps) == 1,
                'd=0 point boundary')
    return {'d_positive_masks': controls, 'd_zero_point_grades': [0, 1, 2, 3]}


def expect_mutation_rejected(label, changed, validator, failures):
    try:
        validator(changed)
    except AssertionError as error:
        failures.append({'mutation': label, 'rejected_by': str(error)})
        return
    raise AssertionError(f'mutation escaped independent validation: {label}')


def mutation_controls(positive_data, boundary_data, expected):
    failures = []
    positive = expected[(1, 1, 1, 1)]
    changed = deepcopy(positive_data)
    changed['certificate']['bad_types'].pop(0)
    expect_mutation_rejected('missing bad type', changed,
                             lambda x: check_positive_payment(x, positive), failures)
    changed = deepcopy(positive_data)
    changed['certificate']['groups'][0]['incoming'][0]['weight'] = '1/2'
    expect_mutation_rejected('wrong rational edge', changed,
                             lambda x: check_positive_payment(x, positive), failures)
    changed = deepcopy(positive_data)
    two_gap = next(edge for edge in changed['all_edges']
                   if len(edge['removed_gap_labels']) == 2)
    two_gap['independent_rows'] = [0, 0]
    expect_mutation_rejected('rank-deficient recovery minor', changed,
                             lambda x: check_positive_payment(x, positive), failures)
    changed = deepcopy(boundary_data)
    changed['cases'][0]['bad_types'].pop(0)
    expect_mutation_rejected('missing boundary bad type', changed,
                             lambda x: check_boundary_payment(x, expected), failures)
    changed = deepcopy(boundary_data)
    changed['cases'][1]['groups'][0]['reserve'][1] = '0'
    expect_mutation_rejected('false boundary reserve', changed,
                             lambda x: check_boundary_payment(x, expected), failures)
    return failures


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def source_identities(paths,index_path):
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads(Path(index_path).read_text())
    indexed={row['path']:row for row in manifest['files']}
    result={}
    for value in paths:
        path=Path(value);relative=path.relative_to(root).as_posix();row=indexed[relative]
        require(path.stat().st_size==row['bytes'] and digest(path)==row['sha256'],'local absorber source changed')
        result[relative]=row['sha256']
    return result


def run_price(bare_records, engine):
    original, caps, parameters = pair_original('22')
    measurements = []
    for t in (1, 12):
        start = time.perf_counter()
        value, statistics = count_original(engine, original, t)
        elapsed = time.perf_counter() - start
        source_rows = {row['t']: row['value'] for row in bare_records['22']['rows']}
        require(value == source_rows[t], 'priced original count differs from source')
        measurements.append({'grade': t, 'value': value,
                             'elapsed_seconds': elapsed, **statistics})
    start = time.perf_counter()
    d, p, delta, _, _ = parameters
    residual = residual_count(12, d, p, delta, caps)
    residual_elapsed = time.perf_counter() - start
    require(residual == measurements[-1]['value'], 'priced residual hard grade')
    start = time.perf_counter()
    band, band_count = actual_band_polynomial(*parameters)
    band_elapsed = time.perf_counter() - start
    require(polynomial_value(band, 12) == residual,
            'priced band hard grade')
    return {'typical_and_hard_original': measurements,
            'hard_residual_elapsed_seconds': residual_elapsed,
            'complete_band_elapsed_seconds': band_elapsed,
            'actual_band_states': band_count,
            'planned_original_rows': 36,
            'degree': len(band) - 1,
            'grade_12_is_extra_unused_holdout': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('price', 'verify'), required=True)
    for option in ('source-index', 'proof', 'tables', 'factor', 'boundary-class',
                   'positive-payment', 'boundary-payment', 'bare11', 'bare12',
                   'bare22', 'original-counter', 'out'):
        parser.add_argument('--' + option, required=True)
    args = parser.parse_args()
    sources = [args.proof, args.tables, args.factor, args.boundary_class,
               args.positive_payment, args.boundary_payment, args.bare11,
               args.bare12, args.bare22]
    identities = source_identities(sources, args.source_index)
    bare = {pair: json.loads(Path(getattr(args, 'bare' + pair)).read_text())
            for pair in ('11', '12', '22')}
    engine = import_original_counter(args.original_counter)
    result = {'mode': args.mode, 'source_copy_sha256': identities,
              'source_index_sha256': digest(args.source_index),
              'original_counter_sha256': digest(args.original_counter),
              'checker_sha256': digest(__file__)}
    if args.mode == 'price':
        result['pricing'] = run_price(bare, engine)
        result['status'] = 'PASS_PRICE_ONLY'
    else:
        factor = json.loads(Path(args.factor).read_text())
        boundary_class = json.loads(Path(args.boundary_class).read_text())
        positive_payment = json.loads(Path(args.positive_payment).read_text())
        boundary_payment = json.loads(Path(args.boundary_payment).read_text())
        classes, descriptions, counts, class_posets = check_classes(
            factor, boundary_class)
        result['type_population'] = counts
        result['complete_type_distinct_posets'] = class_posets
        result['including_connected_factor_posets'] = len(_POLYNOMIALS)
        result['positive_payment'] = check_positive_payment(
            positive_payment, classes[(1, 1, 1, 1)])
        result['boundary_payment'] = check_boundary_payment(boundary_payment,
                                                             classes)
        result['mutations_rejected'] = mutation_controls(
            positive_payment, boundary_payment, classes)
        result['originals'] = check_originals(bare, engine)
        result['zero_controls'] = check_zero_controls(engine)
        result['status'] = 'PASS_INDEPENDENT_FINITE_AND_ORIGINAL_CHECKS'
    with Path(args.out).open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': result['status'],
                      'output': str(args.out),
                      'mode': args.mode,
                      'positive_payment': result.get('positive_payment'),
                      'boundary_payment': result.get('boundary_payment'),
                      'mutations': len(result.get('mutations_rejected', [])),
                      'originals': len(result.get('originals', []))}))


if __name__ == '__main__':
    main()
