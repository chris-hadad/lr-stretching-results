"""Private exact partition/trace validation from the maintained Horn module.

Only these two unchanged functions are required by the split-domain API.
No Horn adoption, census, engine or process interface is imported.
"""

def partition(value):
    if not isinstance(value, (list, tuple)) or any(type(x) is not int or x < 0 for x in value):
        raise ValueError("partitions require exact nonnegative integers")
    if any(a < b for a, b in zip(value, value[1:])):
        raise ValueError("partition is not weakly decreasing")
    out = list(value)
    while out and out[-1] == 0:
        out.pop()
    return out


def triple(lam, mu, nu):
    rows = [partition(x) for x in (lam, mu, nu)]
    if sum(rows[0]) != sum(rows[1]) + sum(rows[2]):
        raise ValueError("unbalanced parent/child triple")
    return rows
