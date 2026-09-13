#!/usr/bin/env python3
"""Derive the two quintic identities and check a labeled non-LR illustration."""
from fractions import Fraction as F
from math import comb


def evaluate(coefficients, t):
    return sum(c * F(t) ** j for j, c in enumerate(coefficients))


def recovered(coefficients):
    # For degree-five reciprocity, I(t) = -P(-t); P(0) = 1.
    a, b = evaluate(coefficients, 1), evaluate(coefficients, 2)
    u, v, w = (-evaluate(coefficients, -t) for t in (1, 2, 3))
    c0 = coefficients[0]
    return ((30*a - 3*b + 60*u - 15*v + 20*c0 + 2*w) / 60,
            (16*(a-u) - (b-v) - 30*c0) / 24)


def main():
    # Basis verification proves the identities for every polynomial of degree <= 5.
    for degree in range(6):
        basis = [F(int(j == degree)) for j in range(6)]
        assert recovered(basis) == (basis[1], basis[2])
    coefficients = [F(1)]
    for root in range(1, 6):
        product = [F(0)] * (len(coefficients) + 1)
        for degree, value in enumerate(coefficients):
            product[degree] += root * value
            product[degree+1] += value
        coefficients = product
    coefficients = [c / 120 for c in coefficients]
    for t in range(1, 9):
        assert evaluate(coefficients, t) == comb(t+5, 5)
        interior = comb(t-1, 5) if t >= 6 else 0
        assert -evaluate(coefficients, -t) == interior
    assert recovered(coefficients) == (F(137, 60), F(15, 8))
    print('PASS: both identities derived on all six monomial basis elements.')
    print('Illustrative simplex polynomial: c1 = 137/60; c2 = 15/8.')
    print('This is an arithmetic illustration, not an additional LR theorem.')


if __name__ == '__main__':
    main()
