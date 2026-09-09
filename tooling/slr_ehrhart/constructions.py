"""Exact combinatorial constructions; no engines or candidate-state operations."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

__all__ = ["skew_content_to_lr", "capped_matrix_to_lr"]


def skew_content_to_lr(
    outer: Sequence[int], inner: Sequence[int], content: Sequence[int],
) -> dict[str, Any]:
    """Lift an entire skew semistandard tableau family to one ordinary LR triple.

    Args:
        outer: Weakly decreasing nonnegative integer partition of the outer shape.
        inner: Such a partition contained in ``outer``, padding with zeros as needed.
        content: Nonempty nonnegative integer composition, in label order 1,...,m,
            whose sum is the skew size. Zero entries retain their alphabet positions.

    Returns:
        A JSON-ready mapping with ``lambda``, ``mu``, ``nu`` and separate ``metadata``.
        Input arrays are copied verbatim into metadata. Only trailing zeros of the
        input/output partitions are normalized away; content is never reordered or
        shortened. Numerical dimension and degree are unknown (``None``).

    Raises:
        ValueError: For invalid sequences, non-integer entries (including bool,
            Fraction and strings), negative entries, malformed partitions, failed
            containment, an empty alphabet or an inconsistent content sum.

    With H=outer[0] (0 for the empty partition), B_i=sum(content[j], j>i)
    for i=1,...,m-1, and kappa_i=sum(content[j], j>=i), the output is
    Lambda=(H+B,outer), Mu=(H repeated m-1 times,inner), Nu=kappa.
    See proofs/skew-lift.md, equation (7).
    Inserting/deleting the fixed superstandard buffer identifies the entire real
    tableau polytopes and their affine integer lattices at every integer stretch
    t>=0. It preserves intrinsic dimension without computing its numerical value.
    This constructor neither evaluates a coefficient nor proves negativity.
    """
    outer_input = _integers(outer, "outer")
    inner_input = _integers(inner, "inner")
    weights = _integers(content, "content")
    lam = _partition(outer_input, "outer")
    mu = _partition(inner_input, "inner")
    if any(part > (lam[i] if i < len(lam) else 0) for i, part in enumerate(mu)):
        raise ValueError("inner must be contained in outer")
    if not weights:
        raise ValueError("content must specify a nonempty ordered alphabet")
    if sum(weights) != sum(lam) - sum(mu):
        raise ValueError("content sum must equal |outer| - |inner|")

    height = lam[0] if lam else 0
    kappa = [0] * len(weights)
    suffix = 0
    for i in range(len(weights) - 1, -1, -1):
        suffix += weights[i]
        kappa[i] = suffix
    buffer = kappa[1:]
    return {
        "lambda": _trim([height + part for part in buffer] + lam),
        "mu": _trim([height] * len(buffer) + mu),
        "nu": _trim(kappa),
        "metadata": {
            "input": {"outer": outer_input, "inner": inner_input, "content": weights},
            "H": height,
            "buffer": buffer,
            "proof": "proofs/skew-lift.md (equation 7)",
            "domain": "entire skew semistandard tableau polytope; ordered alphabet 1,...,m; integer t>=0",
            "lattice_preservation": "insert/delete fixed superstandard buffer tB; affine integer-lattice isomorphism",
            "dimension": None,
            "degree": None,
        },
    }


def capped_matrix_to_lr(row_caps: Sequence[int], column_caps: Sequence[int]) -> dict[str, Any]:
    """Construct one LR triple for the entire nonnegative capped-matrix polytope.

    Both cap vectors must be nonempty sequences of strictly positive Python ints;
    their order is retained. Raises ValueError under the same exact-integer rules
    as skew_content_to_lr. If k=len(row_caps), n=len(column_caps), A=sum(row_caps)
    and B=sum(column_caps), slack completion has margins alpha=(B,*row_caps),
    beta=(A,*column_caps). The beta suffix shape has disconnected rows, whose
    semistandard row counts are precisely the transport matrices of content alpha.
    Reusing skew_content_to_lr then lifts the entire polytope, not a selected face.

    Metadata includes dimension k*n and codegree
    max(ceil((n+1)/a_i), ceil((k+1)/b_j)). A small positive matrix proves full
    dimension in Z^(k*n). At positive integer stretch t, an interior integer
    matrix has entries >=1, row sums <t*a_i and column sums <t*b_j; the all-ones
    matrix witnesses sufficiency of exactly the stated ceiling inequalities.
    Numerical polynomial coefficients and candidate/adoption state are not computed.
    """
    rows = _integers(row_caps, "row_caps")
    columns = _integers(column_caps, "column_caps")
    if not rows or any(value == 0 for value in rows):
        raise ValueError("row_caps must be nonempty and strictly positive")
    if not columns or any(value == 0 for value in columns):
        raise ValueError("column_caps must be nonempty and strictly positive")
    k, n = len(rows), len(columns)
    alpha = [sum(columns)] + rows
    beta = [sum(rows)] + columns
    outer = [0] * len(beta)
    suffix = 0
    for i in range(len(beta) - 1, -1, -1):
        suffix += beta[i]
        outer[i] = suffix
    result = skew_content_to_lr(outer, outer[1:], alpha)
    result["metadata"].update({
        "dimension": k * n,
        "codegree": max(max((n + value) // value for value in rows),
                        max((k + value) // value for value in columns)),
        "capped_matrix": {
            "row_caps": rows,
            "column_caps": columns,
            "transport_row_margins": alpha,
            "transport_column_margins": beta,
            "domain": "all real x_ij>=0 with row sums<=a_i and column sums<=b_j; full Z^(k*n) lattice",
            "lattice_preservation": "unique integral slack completion/deletion, disconnected-row tableau identification, then skew lift",
            "proof": "PROOFS.md#whole-polytope-constructions (whole completion)",
            "source": "PROOFS.md#whole-polytope-constructions (cap completion and interior threshold)",
            "codegree_proof": "interior integer entries>=1 and strict cap inequalities; all-ones matrix is a witness",
        },
    })
    return result


def _integers(values: Sequence[int], name: str) -> list[int]:
    """Copy an exact integer sequence, without coercion or alphabet normalization."""
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes, bytearray)):
        raise ValueError(f"{name} must be a sequence of exact integers")
    result = list(values)
    if any(type(value) is not int for value in result):
        raise ValueError(f"{name} entries must be exact integers (not bool, fractions or strings)")
    if any(value < 0 for value in result):
        raise ValueError(f"{name} entries must be nonnegative")
    return result


def _partition(values: list[int], name: str) -> list[int]:
    if any(left < right for left, right in zip(values, values[1:])):
        raise ValueError(f"{name} must be weakly decreasing")
    return _trim(values)


def _trim(values: list[int]) -> list[int]:
    end = len(values)
    while end and values[end - 1] == 0:
        end -= 1
    return values[:end]
