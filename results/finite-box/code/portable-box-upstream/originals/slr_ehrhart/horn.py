"""Exact multiplicity-one Horn evidence in campaign (outer lambda) convention.

The reduction theorem is Ressayre, reduction.pdf, section 4.1, Theorem 5,
equation (16). Partition walls alone never invoke it. Index partitions use
one-based increasing subsets: tau(I)=(i_r-r,...,i_1-1).
"""
import hashlib
from pathlib import Path
from itertools import combinations
from functools import lru_cache

SOURCE = {
    "theorem": "Ferudun length-at-most-five coefficient nonnegativity",
    "revision": "c3a0795bd287dcca78fac2cc6ba4282144bb7813",
    "dependencies": "earlier a2-a6, ambient top-four, closed-chamber transfer; KTT5 source-audit",
}
HORN_SOURCE = "Ressayre reduction.pdf section 4.1 Theorem 5 equation (16)"


SOURCE_CERTIFICATE_SHA256 = {
    "README.md": "1b9e74abf0d9802c16a68325fd4ff129177024091d480706f942369d989f6aee",
    "verification.json": "3e0253a0a7905442a53f68e4707940c293448c28256e4529cfcddaf90efd39eb",
    "upstream-sha256.json": "c4a7190dea5b596e3eaf4a26281f58f67d3148ceb5f0679367de0ce90ee4a050",
}


def verify_source_roster(paths):
    """Only the exact adopted KTT5 package can enable source-positive records."""
    observed = {}
    for name in paths:
        path = Path(name).resolve(strict=True)
        if path.name in SOURCE_CERTIFICATE_SHA256:
            observed[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    if observed != SOURCE_CERTIFICATE_SHA256:
        raise ValueError("source certificate roster is missing or differs from adopted KTT5 bytes")


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


def index_partition(indices, n):
    if not isinstance(indices, (list, tuple)) or not indices or any(type(i) is not int for i in indices):
        raise ValueError("Horn indices require exact integers")
    if list(indices) != sorted(set(indices)) or indices[0] < 1 or indices[-1] > n:
        raise ValueError("Horn subset is not increasing or is out of range")
    return tuple(i - j for j, i in reversed(list(enumerate(indices, 1))))


@lru_cache(maxsize=4096)
def lr_tableaux(lam, mu, nu):
    """Count LR tableaux exactly; used only for the small Horn index partitions."""
    lam, mu, nu = triple(lam, mu, nu)
    mu += [0] * (len(lam) - len(mu))
    if len(mu) > len(lam) or any(a < b for a, b in zip(lam, mu)):
        return 0
    cells = [(r, c) for r, end in enumerate(lam) for c in range(end - 1, mu[r] - 1, -1)]
    used, filled = [0] * len(nu), {}
    def visit(k):
        if k == len(cells):
            return 1
        r, c = cells[k]
        total = 0
        for label in range(len(nu)):
            if used[label] == nu[label] or (label and used[label] == used[label - 1]):
                continue
            if (r, c + 1) in filled and label > filled[r, c + 1]:
                continue
            if (r - 1, c) in filled and label <= filled[r - 1, c]:
                continue
            used[label] += 1; filled[r, c] = label
            total += visit(k + 1)
            used[label] -= 1; del filled[r, c]
        return total
    return visit(0)


def verify_horn(lam, mu, nu, evidence):
    """Rebuild the inequality, multiplicity, equality and children; reject tampering."""
    rows = triple(lam, mu, nu)
    n = max(map(len, rows), default=0)
    if n < 2 or n > 7:
        raise ValueError("Horn terminal supports exact ranks 2 through 7")
    if evidence.get("orientation") != "lambda[K]<=mu[I]+nu[J]":
        raise ValueError("wrong Horn orientation")
    I, J, K = (evidence.get(key) for key in ("I", "J", "K"))
    a, b, c = (index_partition(indices, n) for indices in (I, J, K))
    if not (len(I) == len(J) == len(K) < n):
        raise ValueError("Horn subsets must have the same proper size")
    if sum(c) != sum(a) + sum(b) or lr_tableaux(c, a, b) != 1:
        raise ValueError("Horn index multiplicity is not one")
    padded = [row + [0] * (n - len(row)) for row in rows]
    subsets = [K, I, J]
    children = []
    for complement in (False, True):
        child = [[x for i, x in enumerate(row, 1) if (i in idx) != complement]
                 for row, idx in zip(padded, subsets)]
        children.append(triple(*child))  # selected equality and complement balance
    if "children" in evidence and evidence["children"] != children:
        raise ValueError("tampered Horn children")
    if "multiplicity" in evidence and (type(evidence["multiplicity"]) is not int or evidence["multiplicity"] != 1):
        raise ValueError("tampered Horn multiplicity")
    unresolved = [child for child in children if max(map(len, child)) > 5]
    return {"kind": "horn_factorization", "source": HORN_SOURCE,
            "orientation": evidence["orientation"], "I": list(I), "J": list(J), "K": list(K),
            "multiplicity": 1, "index_partitions": [list(a), list(b), list(c)],
            "children": children, "unresolved_children": unresolved,
            "identity": "P_parent=P_selected*P_complement", "all_stretches": True}


def source_terminal(lam, mu, nu, p1=None, witness=None):
    rows = triple(lam, mu, nu)
    if p1 is not None and (type(p1) is not int or p1 < 0):
        raise ValueError("P1 must be an exact nonnegative integer")
    if p1 == 0:
        return {"evidence_kind": "empty_hive", "source": "saturation", "zero_polynomial": True}
    n = max(map(len, rows), default=0)
    positivity = {"coefficient_nonnegative": True, "nonemptiness": "known_nonempty" if p1 else "unknown"}
    if p1:
        positivity["constant_term"] = 1
    if n <= 5:
        return {"evidence_kind": "source_theorem_positive", "source": SOURCE, "rank": n,
                **positivity}
    if witness is not None:
        reduction = verify_horn(*rows, witness)
    elif n <= 7:
        padded = [row + [0] * (n - len(row)) for row in rows]
        reduction = None
        for size in range(1, n // 2 + 1):
            subsets = list(combinations(range(1, n + 1), size))
            for I in subsets:
                for J in subsets:
                    required = sum(I) + sum(J) - size * (size + 1) // 2
                    rhs = sum(padded[1][i - 1] for i in I) + sum(padded[2][j - 1] for j in J)
                    for K in subsets:
                        if sum(K) != required or sum(padded[0][k - 1] for k in K) != rhs:
                            continue
                        try:
                            candidate = verify_horn(*rows, {"orientation": "lambda[K]<=mu[I]+nu[J]",
                                                          "I": I, "J": J, "K": K})
                        except ValueError:
                            continue
                        reduction = candidate
                        if not candidate["unresolved_children"]:
                            return {"evidence_kind": "source_theorem_positive", "source": SOURCE,
                                    **positivity, "reduction": reduction}
        if reduction is None:
            return {"evidence_kind": "unresolved", "reason": "no multiplicity-one tight Horn witness"}
    else:
        return {"evidence_kind": "unresolved", "reason": "rank exceeds terminal domain"}
    return {"evidence_kind": "unresolved" if reduction["unresolved_children"] else "source_theorem_positive",
            "source": SOURCE, "reduction": reduction,
            **({**positivity}
               if not reduction["unresolved_children"] else {})}
