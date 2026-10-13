"""Exact LR row-state count for any outer rank and at most three content letters.

This counts the full original skew tableau, with lambda the outer shape.
No source-family formula, cap hypothesis, or returned provider code is used.
"""
from functools import lru_cache


def _partition(values, name):
    if not isinstance(values, (tuple, list)):
        raise ValueError(f"{name} must be a sequence")
    if any(type(x) is not int or x < 0 for x in values):
        raise ValueError(f"{name} requires exact nonnegative integers")
    if any(a < b for a, b in zip(values, values[1:])):
        raise ValueError(f"{name} must be weakly decreasing")
    result = tuple(values)
    while result and result[-1] == 0:
        result = result[:-1]
    return result


def _triple(outer, inner, content):
    lam = _partition(outer, "outer")
    mu = _partition(inner, "inner")
    nu = _partition(content, "content")
    if len(nu) > 3:
        raise ValueError("at most three positive content letters are supported")
    if sum(lam) != sum(mu) + sum(nu):
        raise ValueError("the original triple must be balanced")
    return lam, mu, nu


def lr_count(outer, inner, content, *, statistics=None, max_states=None):
    """Return the exact bare-triple LR coefficient.

    Malformed or unbalanced triples raise ValueError; balanced but infeasible
    triples return zero. A zero-cell tableau counts once. A state ceiling raises
    RuntimeError before a partial count can be reported.
    """
    lam, mu, nu = _triple(outer, inner, content)
    if max_states is not None and (type(max_states) is not int or max_states < 0):
        raise ValueError("max_states must be a nonnegative integer")
    if len(mu) > len(lam) or any(a < b for a, b in zip(lam, mu)):
        if statistics is not None:
            statistics.update(states=0, transitions=0, cache_hits=0)
        return 0
    n = len(lam)
    mu += (0,) * (n - len(mu))
    nu += (0,) * (3 - len(nu))
    area = [0]
    for top, bottom in zip(lam, mu):
        area.append(area[-1] + top - bottom)
    if n == 0 or area[-1] == 0:
        if statistics is not None:
            statistics.update(states=0, transitions=0, cache_hits=0)
        return 1

    transitions = 0
    states = 0

    @lru_cache(maxsize=None)
    def visit(i, used_two, used_three, previous_one, previous_two):
        nonlocal transitions, states
        states += 1
        if max_states is not None and states > max_states:
            raise RuntimeError(f"LR state ceiling {max_states} exceeded")
        used_one = area[i] - used_two - used_three
        if i == n:
            return int((used_one, used_two, used_three) == nu)
        width = lam[i] - mu[i]
        if i:
            gap = mu[i - 1] - mu[i]
            # For each j=1,2,3:
            # mu_(i-1) + sum_(k<j) a_(i-1,k)
            #     >= mu_i + sum_(k<=j) a_(i,k).
            limit_one = gap
            limit_two = gap + previous_one
            limit_three = limit_two + previous_two
            if width > limit_three:
                return 0
            z_low = max(0, width - limit_two)
        else:
            limit_one = width
            z_low = 0
        z_high = min(width, nu[2] - used_three, used_two - used_three)
        total = 0
        for z in range(z_low, z_high + 1):
            y_low = max(0, width - z - (nu[0] - used_one),
                        width - z - limit_one)
            y_high = min(width - z, nu[1] - used_two, used_one - used_two)
            for y in range(y_low, y_high + 1):
                x = width - y - z
                # z and y ballot bounds above are checked at the right-to-left
                # word prefixes where all 3s and then all 2s have been read.
                transitions += 1
                total += visit(i + 1, used_two + y, used_three + z, x, y)
        return total

    result = visit(0, 0, 0, 0, 0)
    if statistics is not None:
        statistics.update(states=states, transitions=transitions,
                          cache_hits=visit.cache_info().hits)
    return result


def stretched_lr_count(outer, inner, content, t, *, statistics=None,
                       max_states=None):
    """Count a stretch; t=0 follows the nonempty-hive/zero-polynomial convention.

    At zero, return one exactly when the balanced original triple has a
    positive grade-one count, and zero otherwise. This differs from counting
    the all-zero triple literally for an infeasible original.
    """
    lam, mu, nu = _triple(outer, inner, content)
    if type(t) is not int or t < 0:
        raise ValueError("t must be an exact nonnegative integer")
    if t == 0:
        return int(lr_count(lam, mu, nu, statistics=statistics,
                            max_states=max_states) > 0)
    return lr_count(tuple(t * x for x in lam), tuple(t * x for x in mu),
                    tuple(t * x for x in nu), statistics=statistics,
                    max_states=max_states)
