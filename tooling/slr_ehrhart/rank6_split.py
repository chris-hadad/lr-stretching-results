"""An exact ordinary LR count on one complete principal 3+3 split domain.

Lambda is outer. The source-defined affine row-count chart below retains all
21 nonnegativity, 15 column and 15 ballot inequalities. Their minima define
a sufficient boundary domain; refusal says nothing about LR feasibility or
coefficient signs outside it. Inner partitions are never swapped implicitly.
This is a rank-at-most-six chart, not a general-rank or whole-rank-six cover.
"""
from __future__ import annotations

from fractions import Fraction

from ._partitions import triple
from .two_widths import two_width_count, two_width_polynomial

__all__ = ['rank6_split_parameters', 'rank6_split_count', 'rank6_split_polynomial']

_WIDTH = 29  # lambda, mu, nu (six each), nine cross counts, s, v
_ZERO = (0,) * _WIDTH
_LEFT = (0, 0, 1) * 3
_RIGHT = (1, 1, 1, 0, 0, 0, 0, 0, 0)


def _unit(index):
    return tuple(int(j == index) for j in range(_WIDTH))


def _add(*rows):
    return tuple(map(sum, zip(*rows))) if rows else _ZERO


def _scale(coefficient, row):
    return tuple(coefficient * value for value in row)


def _minus(left, right):
    return _add(left, _scale(-1, right))


def _build_chart():
    """Build the complete integer chart and every exact inequality minimum.

    x[i,j] counts label j+1 in row i+1 of an LR tableau. The nine cross
    coordinates are x[i+3,j] for 0<=i,j<3; they sum to S. The two remaining
    coordinates are s=x[2,1] and v=x[4,3], with bounds
    0<=s<=A+cross_column_3 and 0<=v<=B+cross_row_1. All other row counts
    follow affinely. The inverse reads these selected row counts directly.

    First minimize each parent inequality over both interval endpoints, then
    over the cross simplex. This gives one boundary form per parent inequality,
    including redundant and zero forms. No external proof data is loaded.
    """
    lam, mu, nu = [tuple(_unit(offset + i) for i in range(6)) for offset in (0, 6, 12)]
    length = tuple(_minus(a, b) for a, b in zip(lam, mu))
    S = _add(*mu[:3], *nu[:3], *[_scale(-1, value) for value in lam[:3]])
    A = _add(lam[2], _scale(-1, mu[2]), _scale(-1, nu[2]))
    B = _add(mu[3], nu[3], _scale(-1, lam[3]))
    cross = [_unit(18 + i) for i in range(9)]
    rows = [_add(*cross[3 * i:3 * i + 3]) for i in range(3)]
    cols = [_add(*cross[j::3]) for j in range(3)]
    s, v = _unit(27), _unit(28)
    x = {(i, j): _ZERO for i in range(6) for j in range(6)}
    x[0, 0] = length[0]
    x[1, 0] = _add(length[1], _scale(-1, nu[1]), cols[1], s)
    x[1, 1] = _add(nu[1], _scale(-1, cols[1]), _scale(-1, s))
    x[2, 0] = _add(A, cols[2], _scale(-1, s))
    x[2, 1] = s
    x[2, 2] = _minus(nu[2], cols[2])
    for i in range(3):
        for j in range(3):
            x[i + 3, j] = cross[3 * i + j]
    x[3, 3] = _minus(length[3], rows[0])
    x[4, 3] = v
    x[4, 4] = _add(length[4], _scale(-1, rows[1]), _scale(-1, v))
    x[5, 3] = _add(B, rows[0], _scale(-1, v))
    x[5, 4] = _add(nu[4], _scale(-1, length[4]), rows[1], v)
    x[5, 5] = nu[5]
    constraints = [(f'nonnegative_{i + 1}_{j + 1}', x[i, j])
                   for i in range(6) for j in range(i + 1)]
    for i in range(1, 6):
        for j in range(i):
            form = _add(mu[i - 1], _scale(-1, mu[i]),
                        *[x[i - 1, k] for k in range(j)],
                        *[_scale(-1, x[i, k]) for k in range(j + 1)])
            constraints.append((f'column_{i + 1}_{j + 1}', form))
    for j in range(5):
        for i in range(j + 1, 6):
            form = _add(*[x[r, j] for r in range(i)],
                        *[_scale(-1, x[r, j + 1]) for r in range(i + 1)])
            constraints.append((f'ballot_{i + 1}_{j + 1}', form))
    assert len(constraints) == 51
    domain = []
    for name, form in constraints:
        e, f = min(form[27], 0), min(form[28], 0)
        coefficients = [form[18 + k] + e * _LEFT[k] + f * _RIGHT[k] for k in range(9)]
        minimum = _add(form[:18] + (0,) * 11, _scale(e, A), _scale(f, B),
                       _scale(min(coefficients), S))
        domain.append((name, minimum[:18]))
    return {'parameters': {'S': S, 'A': A, 'B': B}, 'row_counts': x,
            'constraints': tuple(constraints), 'domain': tuple(domain)}


_CHART = _build_chart()


def rank6_split_parameters(lam, mu, nu) -> dict[str, int]:
    """Validate the full domain and return exact nonnegative S, A and B.

    Use strict partition and trace validation, trim trailing zeros and pad to
    six. Here S=sum(mu[:3])+sum(nu[:3])-sum(lambda[:3]),
    A=lambda[2]-mu[2]-nu[2] and B=mu[3]+nu[3]-lambda[3]. A valid partition
    triple still must pass the nonnegative parameter gate and all 51 boundary
    minima. Invalid or unsupported triples raise ValueError, including at t=0.
    """
    parts = triple(lam, mu, nu)
    if max(map(len, parts)) > 6:
        raise ValueError('the principal split chart supports rank at most six')
    boundary = tuple(value for part in parts for value in part + [0] * (6 - len(part)))
    values = {name: sum(coefficient * value for coefficient, value in zip(form, boundary))
              for name, form in _CHART['parameters'].items()}
    if min(values.values()) < 0:
        raise ValueError('triple is outside the nonnegative S, A, B chart domain')
    for name, form in _CHART['domain']:
        slack = sum(coefficient * value for coefficient, value in zip(form, boundary))
        if slack < 0:
            raise ValueError(f'triple is outside the full split domain at {name}: {slack}')
    return values


def rank6_split_count(lam, mu, nu, t: int = 1) -> int:
    """Count the complete stretched ordinary LR object on the admitted domain.

    The exact identity is binom(S*t+8,8)*(1+(A+S/3)*t)*(1+(B+S/3)*t).
    All degenerations are retained. The original triple is validated even
    when t=0; t must be a nonnegative exact Python integer, excluding bools.
    """
    p = rank6_split_parameters(lam, mu, nu)
    return two_width_count(_LEFT, _RIGHT, total=p['S'], left_offset=p['A'],
                           right_offset=p['B'], dilation=t)


def rank6_split_polynomial(lam, mu, nu) -> tuple[Fraction, ...]:
    """Return the whole supported LR polynomial as low-to-high Fractions.

    The complete integer row-count chart supplies the all-stretch identity.
    Its degree is at most ten; the exact symbolic expansion removes trailing
    zeros, including the S=0 cases. No samples determine the degree or count.
    """
    p = rank6_split_parameters(lam, mu, nu)
    return two_width_polynomial(_LEFT, _RIGHT, total=p['S'], left_offset=p['A'],
                                right_offset=p['B'])
