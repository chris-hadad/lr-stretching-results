"""A certified bare-triple count path on one explicit rank-six boundary sector.

The complete Cdagger domain retains 521 Horn, 18 partition and 17 source
facet inequalities, represented by 553 distinct trace-chart rows. Outside
this sufficient domain the API refuses; it makes no assertion of infeasibility
or coefficient signs. It does not search or cover all rank six.
"""
from __future__ import annotations

from fractions import Fraction

from . import _cdagger_data as data
from .constructions import _integers, _partition
from .strip import strip_count, strip_polynomial

__all__ = ['OutsideCdaggerError', 'cdagger_parameters', 'cdagger_count',
           'cdagger_polynomial', 'verify_cdagger_certificate']


class OutsideCdaggerError(ValueError):
    """The valid triple is outside this proved sufficient count domain."""


def cdagger_parameters(lam, mu, nu) -> dict[str, int]:
    """Validate the entire domain and return its exact integer strip parameters.

    Lambda is outer. Partition inputs obey the constructors' exact-integer
    convention, trim trailing zeros and are padded to six. Invalid partitions
    or size balance raise ValueError. A valid triple of rank above six, or one
    violating a Cdagger domain row, raises OutsideCdaggerError. Inner partitions
    are never swapped implicitly. No gate failure is converted into count zero.
    """
    parts = [_partition(_integers(part, name), name)
             for part, name in ((lam, 'lambda'), (mu, 'mu'), (nu, 'nu'))]
    if sum(parts[0]) != sum(parts[1]) + sum(parts[2]):
        raise ValueError('|lambda| must equal |mu|+|nu|')
    if max(map(len, parts)) > 6:
        raise OutsideCdaggerError('the certified Cdagger chart has padded rank six')
    boundary = tuple(value for part in parts for value in part + [0] * (6 - len(part)))
    for index, row in enumerate(data.DOMAIN_ROWS):
        if sum(coefficient * boundary[j] for j, coefficient in row) < 0:
            raise OutsideCdaggerError(f'triple is outside Cdagger at domain row {index}')
    values = {name: sum(coefficient * boundary[j] for j, coefficient in row)
              for name, row in data.PHYSICAL_ROWS.items()}
    if any(value < 0 for value in values.values()):
        raise RuntimeError('certified Cdagger parameter implication failed')
    return {name: values[name] for name in ('x', 'T', 'Bcap', 'C', 'D')}


def cdagger_count(lam, mu, nu, t: int = 1) -> int:
    """Count the entire stretched ordinary LR hive on the certified domain.

    The all-parameter unimodular hive/strip map supplies the count identity.
    t must be a nonnegative exact Python integer, including t=0. The original
    triple must pass the domain even at t=0; an unsupported input is refused.
    """
    if type(t) is not int or t < 0:
        raise ValueError('t must be a nonnegative exact Python integer')
    p = cdagger_parameters(lam, mu, nu)
    return strip_count(3, 3, 3, p['T'], p['Bcap'], p['C'], p['D'], t,
                       interval_lengths=(p['x'],))


def cdagger_polynomial(lam, mu, nu) -> tuple[Fraction, ...]:
    """Return all ordinary coefficients of the whole supported LR polynomial.

    The proved count identity has degree at most ten, including dimension
    drops. Exact finite differences recover it at that proved bound, with
    trailing zero coefficients removed. This is a specialized theorem path,
    not a fit whose degree or full-hive premise is inferred from scalar values.
    """
    p = cdagger_parameters(lam, mu, nu)
    return strip_polynomial(3, 3, 3, p['T'], p['Bcap'], p['C'], p['D'],
                            interval_lengths=(p['x'],))


def verify_cdagger_certificate() -> dict[str, int]:
    """Replay the 36 exact implications against the complete conventional hive.

    This checks the shipped fixed proof data, not an untrusted general-purpose
    certificate schema. No optimizer, vertex enumeration or native count runs.
    Failure raises ValueError. Success authenticates all six parameter and all
    thirty omitted-rhombus identities, and the complete integer slack chart.
    """
    from .hive import hive_linear_system

    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def dense(row, width):
        result = [Fraction(0)] * width
        require(len(row) == len({index for index, _ in row}), 'duplicate sparse index')
        for index, value in row:
            require(type(index) is int and 0 <= index < width, 'invalid sparse index')
            result[index] = Fraction(value)
        return result

    def multiply(left, right):
        columns = tuple(zip(*right))
        return [[sum(a * b for a, b in zip(row, column)) for column in columns] for row in left]

    A, B, dimension = hive_linear_system(6)
    require(dimension == 10 and len(A) == len(B) == 45, 'wrong complete hive shape')
    require(len(data.DOMAIN_ROWS) == 553, 'incomplete fixed domain row roster')
    domain = [dense(row, 18) for row in data.DOMAIN_ROWS]
    basis = data.BASIS_ROWS
    require(len(basis) == len(set(basis)) == 10, 'incomplete basis row roster')
    U = [A[index] for index in basis]
    inverse = data.U_INVERSE
    require(len(inverse) == 10 and all(len(row) == 10 for row in inverse), 'wrong inverse shape')
    require(all(type(value) is int for row in inverse for value in row), 'nonintegral inverse')
    identity = [[int(i == j) for j in range(10)] for i in range(10)]
    require(multiply(U, inverse) == identity and multiply(inverse, U) == identity,
            'slack chart is not an integer lattice automorphism')
    N = multiply(A, inverse)
    transformed_boundary = multiply(N, [B[index] for index in basis])
    K = [[value - correction for value, correction in zip(row, removed)]
         for row, removed in zip(B, transformed_boundary)]
    physical = {name: dense(row, 18) for name, row in data.PHYSICAL_ROWS.items()}
    require(set(physical) == {'x', 'T', 'Bcap', 'C', 'D', 'Bcap+C+D-T'}, 'physical roster differs')
    expected_physical = {'x': K[24], 'T': K[44], 'Bcap': K[20], 'D': K[32],
                         'C': [a - b for a, b in zip(K[9], K[32])]}
    expected_physical['Bcap+C+D-T'] = [
        b + c + d - t for b, c, d, t in zip(expected_physical['Bcap'], expected_physical['C'],
                                          expected_physical['D'], expected_physical['T'])]
    require(physical == expected_physical, 'physical forms differ from whole-hive chart')
    model = data.MODEL_ROWS
    require(len(model) == len(set(model)) == 15
            and set(model) == set(basis) | {9, 20, 24, 32, 44}, 'model row roster differs')
    expected = {row: (identity[j], [0] * 18) for j, row in enumerate(basis)}

    def row(entries):
        return [entries.get(j, 0) for j in range(10)]

    expected.update({
        24: (row({8: -1}), physical['x']),
        44: (row({j: -1 for j in (1, 2, 3, 4, 5, 6, 7, 9)}), physical['T']),
        20: (row({0: 1, 3: -1, 5: -1, 6: -1}), physical['Bcap']),
        32: (row({0: -1, **{j: 1 for j in range(1, 7)}}), physical['D']),
        9: (row({0: -1}), [c + d for c, d in zip(physical['C'], physical['D'])]),
    })
    require(all((N[index], K[index]) == expected[index] for index in model),
            'selected rows are not the stated whole strip')
    combined = [[0] * 10 + values for values in domain] + [N[index] + K[index] for index in model]
    targets = {name: ('physical_parameter', values) for name, values in physical.items()}
    targets.update({f'omitted_raw_row_{index}': ('omitted_hive', N[index] + K[index])
                    for index in range(45) if index not in set(model)})
    require(len(data.DUALS) == 36 and len({item[0] for item in data.DUALS}) == 36
            and {item[0] for item in data.DUALS} == set(targets), 'incomplete or duplicate implication roster')
    trace = [1] * 6 + [-1] * 12
    for name, kind, sparse, equality in data.DUALS:
        expected_kind, target = targets[name]
        require(kind == expected_kind, 'implication kind mismatch')
        base = domain if kind == 'physical_parameter' else combined
        multipliers = dense(sparse, len(base))
        require(all(value >= 0 for value in multipliers), 'negative inequality multiplier')
        total = [sum(weight * values[j] for weight, values in zip(multipliers, base))
                 for j in range(len(target))]
        trace_row = trace if kind == 'physical_parameter' else [0] * 10 + trace
        require([value + Fraction(equality) * coefficient for value, coefficient in zip(total, trace_row)] == target,
                f'false ambient implication: {name}')
    return {'domain_rows': len(domain), 'hive_rows': 45, 'model_rows': 15,
            'parameter_implications': 6, 'omitted_hive_implications': 30,
            'integer_chart_dimension': 10}
