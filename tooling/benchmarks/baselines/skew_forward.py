"""Frozen selected native counting functions; benchmark comparison only."""
from __future__ import annotations
import time

def horizontal_strips(nu: tuple[int, ...], lam: tuple[int, ...], size: int) -> list[tuple[int, ...]]:
    """Every partition nu' with nu ⊆ nu' ⊆ lam, |nu'/nu| = size and nu'/nu a horizontal strip."""
    k = len(lam)
    out: list[tuple[int, ...]] = []

    def rec(i: int, remaining: int, acc: list[int]) -> None:
        if i == k:
            if remaining == 0:
                out.append(tuple(acc))
            return
        lo = nu[i]
        hi = min(lam[i], nu[i - 1] if i > 0 else lam[i])  # a horizontal strip: nu'_i <= nu_{i-1}
        # the rows below can absorb at most sum_{r > i} (min(lam[r], nu[r-1]) - nu[r]) more boxes, so prune
        for x in range(lo, hi + 1):
            add = x - lo
            if add > remaining:
                break
            acc.append(x)
            rec(i + 1, remaining - add, acc)
            acc.pop()

    rec(0, size, [])
    return out

def count(alpha: list[int], beta: list[int], w: list[int], T: int) -> tuple[int, int, float]:
    """K(T·alpha / T·beta, T·w) by the strip recursion; returns (count, max states seen, seconds)."""
    t0 = time.monotonic()
    lam = tuple(T * a for a in alpha)
    mu = tuple(T * b for b in beta) + (0,) * (len(alpha) - len(beta))
    states: dict[tuple[int, ...], int] = {mu: 1}
    max_states = 1
    for wj in w:
        size = T * wj
        nxt: dict[tuple[int, ...], int] = {}
        for nu, ways in states.items():
            for nu2 in horizontal_strips(nu, lam, size):
                nxt[nu2] = nxt.get(nu2, 0) + ways
        states = nxt
        max_states = max(max_states, len(states))
        if not states:
            break
    return states.get(lam, 0), max_states, round(time.monotonic() - t0, 4)
