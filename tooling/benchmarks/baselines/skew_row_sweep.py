"""Frozen selected native counting functions; benchmark comparison only."""
from __future__ import annotations
from collections import defaultdict

def strip_kostka(alpha: list[int], beta: list[int], w: list[int]) -> int:
    n = len(alpha)
    beta = list(beta) + [0] * (n - len(beta))
    cap = list(alpha)
    # level state: tuple nu (length n), value = number of chains reaching it
    cur: dict[tuple[int, ...], int] = {tuple(beta): 1}
    for step, size in enumerate(w):
        # bottom-up row sweep; carry a budget of how much of `size` has been spent
        # sweep state: (tuple, spent) where rows i..n-1 already hold nu', rows 0..i-1 hold nu
        state: dict[tuple[tuple[int, ...], int], int] = {(k, 0): v for k, v in cur.items()}
        for i in range(n - 1, -1, -1):
            nxt: dict[tuple[tuple[int, ...], int], int] = defaultdict(int)
            for (nu, spent), cnt in state.items():
                lo = nu[i]
                hi = cap[i] if i == 0 else min(nu[i - 1], cap[i])
                room = size - spent
                top = min(hi, lo + room)
                for val in range(lo, top + 1):
                    nu2 = nu[:i] + (val,) + nu[i + 1:]
                    nxt[(nu2, spent + val - lo)] += cnt
            state = nxt
        cur = defaultdict(int)
        for (nu, spent), cnt in state.items():
            if spent == size:
                cur[nu] += cnt
        if not cur:
            return 0
    return cur.get(tuple(alpha), 0)
