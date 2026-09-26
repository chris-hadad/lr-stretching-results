"""Exact original_rows body from the accepted structural mask checker."""
from functools import lru_cache

def require(test, message):
    if not test:
        raise ValueError(message)

@lru_cache(None)
def original_rows(n):
    """Full boundary-linear rhombi in the accepted F025 up/down row order."""
    require(type(n) is int and 2 <= n <= 7, "Unsupported original hive rank")
    interior = [(i, j) for i in range(1, n) for j in range(1, n-i)]
    pos = {p: i for i, p in enumerate(interior)}
    width = 3*n + len(interior)
    values = {}
    for i in range(n+1):
        for j in range(n+1-i):
            row = [0]*width
            if (i, j) in pos:
                row[3*n+pos[i,j]] = 1
            elif j == 0:
                for k in range(i):
                    row[n+k] = 1
            elif i == 0:
                for k in range(j):
                    row[k] = 1
            else:
                for k in range(n):
                    row[n+k] = 1
                for k in range(j):
                    row[2*n+k] = 1
            values[i,j] = row
    stencils = []
    for i in range(n):
        for j in range(n-i):
            if i+j < n-1:
                stencils.append((((i+1,j),1),((i,j+1),1),((i,j),-1),((i+1,j+1),-1)))
            if j:
                stencils.append((((i,j),1),((i+1,j),1),((i,j+1),-1),((i+1,j-1),-1)))
            if i:
                stencils.append((((i,j),1),((i,j+1),1),((i+1,j),-1),((i-1,j+1),-1)))
    require(len(stencils) == 3*n*(n-1)//2, "Incomplete original rhombus roster")
    require(len({tuple(sorted(s)) for s in stencils}) == len(stencils), "Duplicate original rhombus")
    return tuple(tuple(sum(sign*values[p][c] for p, sign in stencil) for c in range(width))
                 for stencil in stencils)
