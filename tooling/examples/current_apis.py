"""Small published controls for the current standalone APIs; no output files."""
from pathlib import Path
from fractions import Fraction
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from slr_ehrhart import (
    rank6_split_parameters, rank6_split_count, rank6_split_polynomial,
    rank8_clipped_boundary, rank8_clipped_count, rank8_clipped_polynomial,
    rectangular_matrix_invariant_count, two_width_count, two_width_polynomial,
)

def main():
    boundary = ((9, 8, 6, 4, 2, 1), (5, 4, 3, 2, 1), (5, 4, 3, 2, 1))
    print("Rank-six split parameters:", rank6_split_parameters(*boundary))
    count = rank6_split_count(*boundary)
    assert count == 16
    print("Rank-six P(1):", count)
    print("Rank-six complete vector:", tuple(map(str, rank6_split_polynomial(*boundary))))

    print("Clipped rank-eight boundary:", rank8_clipped_boundary(1, 2))
    assert rank8_clipped_count(1, 2) == 1678
    vector = rank8_clipped_polynomial(1, 2)
    assert len(vector) == 22
    print("Clipped rank-eight P(1):", 1678)
    print("Clipped rank-eight complete vector:", tuple(map(str, vector)))

    rectangular = rectangular_matrix_invariant_count(
        2, 3, 3, 1, max_states=100000, max_transitions=1000000)
    assert rectangular == 20
    print("Three labeled 2-by-3 matrices, entry degree 6:", rectangular)

    # This complete abstract polytope has no claimed LR realization.
    vector = two_width_polynomial((7, 0), (0, 7))
    assert vector == (Fraction(1), Fraction(-1, 6), Fraction(7), Fraction(49, 6))
    assert two_width_count((7, 0), (0, 7)) == 16
    print("Abstract two-width vector (not an LR counterexample):", tuple(map(str, vector)))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

