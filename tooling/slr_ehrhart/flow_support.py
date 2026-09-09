"""Exact feasibility and dimension certificates for a unique-edge interval flow.

The fiber is x >= 0 with sum(x[e] for e=(u,v) if u <= i < v) = totals[i].
This certifies that entire bounded integral flow polytope. Transferring its
degree to an LR family needs a separate entire-polytope and lattice argument.
No LR inverse, coefficient computation, or positivity claim is supplied here.

Extracted from the verified FRC sparse flow certificates; see FLOW-SUPPORT.md
for the proof and the supported input and certificate contracts.
"""

from collections import deque
from fractions import Fraction

__all__ = ["flow_support_certificate", "verify_flow_support_certificate"]


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _integer(value, name, minimum=None, maximum=None):
    _require(type(value) is int, f"{name} must be an exact Python integer")
    _require(minimum is None or value >= minimum, f"{name} is below its minimum")
    _require(maximum is None or value <= maximum, f"{name} exceeds its maximum")
    return value


def _inputs(interval_edges, totals):
    _require(type(totals) in (list, tuple), "totals must be a list or tuple")
    target = tuple(_integer(x, f"totals[{i}]") for i, x in enumerate(totals))
    _require(type(interval_edges) in (list, tuple),
             "interval_edges must be a list or tuple")
    edges = []
    for i, edge in enumerate(interval_edges):
        _require(type(edge) in (list, tuple) and len(edge) == 2,
                 f"interval_edges[{i}] must be a pair")
        u = _integer(edge[0], f"interval_edges[{i}][0]", 0, len(target))
        v = _integer(edge[1], f"interval_edges[{i}][1]", 0, len(target))
        _require(u < v, f"interval_edges[{i}] must satisfy u < v")
        edges.append((u, v))
    _require(len(edges) == len(set(edges)), "duplicate interval edges are unsupported")
    return tuple(edges), target


def _balances(totals):
    # Outgoing minus incoming incidence, also valid for the empty system.
    padded = (0,) + tuple(totals) + (0,)
    return [right - left for left, right in zip(padded, padded[1:])]


def _search(adjacency, start):
    previous = {start: None}
    todo = deque([start])
    while todo:
        u = todo.popleft()
        for v in adjacency[u]:
            if v not in previous:
                previous[v] = u
                todo.append(v)
    return previous


def _path(previous, target):
    path = [target]
    while previous[path[-1]] is not None:
        path.append(previous[path[-1]])
    path.reverse()
    return path


def _cut_capacity(edges, balances, supply, cut):
    return (sum(supply for u, v in edges if u in cut and v not in cut)
            + sum(b for u, b in enumerate(balances) if b > 0 and u not in cut)
            + sum(-b for u, b in enumerate(balances) if b < 0 and u in cut))


def _components(vertex_count, edges):
    parent = list(range(vertex_count))

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u, v in edges:
        parent[find(u)] = find(v)
    return len({find(v) for v in range(vertex_count)})


def _interval_rank(n, edges):
    """Independent exact elimination on the original interval columns."""
    basis = {}
    for u, v in edges:
        row = [Fraction(int(u <= i < v)) for i in range(n)]
        for pivot in range(n):
            coefficient = row[pivot]
            if not coefficient:
                continue
            if pivot in basis:
                for j in range(pivot, n):
                    row[j] -= coefficient * basis[pivot][j]
            else:
                basis[pivot] = [entry / coefficient for entry in row]
                break
    return len(basis)


def flow_support_certificate(interval_edges, totals):
    """Return a checked, JSON-ready certificate for the specified flow fiber.

    Inputs are lists or tuples; every edge is a two-entry list or tuple with
    exact Python integers 0 <= u < v <= len(totals). Endpoints may not repeat
    as a pair: parallel variables are outside this API. The original position
    is the edge identity. Totals are exact Python integers, including zero or
    negative entries; a negative total has an infeasible fiber. Bools, floats,
    strings, coercions, and invalid structures raise ValueError.

    A feasible result includes a complete integral flow, active edge indices,
    a residual-cycle path for each active zero entry, a closed cut for every
    forced-zero edge, rank, components including isolated vertices, dimension,
    and Ehrhart degree. An infeasible result includes an augmented source/sink
    cut with capacity strictly below the total supply; it has no degree field.
    Empty edges and empty or zero totals are supported.

    Results use only new dictionaries/lists, strings, exact ints, and a bool.
    They bind copied edges and totals and are deterministic for the same input.
    No input is mutated, no native tools are used, and there is no sampling,
    global cache, or internal time limit. Bound execution externally as needed.
    """
    edges, target = _inputs(interval_edges, totals)
    n = len(target)
    balances = _balances(target)
    supply = sum(max(b, 0) for b in balances)
    source, sink = n + 1, n + 2
    residual = [{} for _ in range(n + 3)]

    def arc(u, v, capacity):
        residual[u][v] = capacity
        residual[v][u] = 0

    for u, v in edges:
        arc(u, v, supply)
    for u, balance in enumerate(balances):
        if balance > 0:
            arc(source, u, balance)
        elif balance < 0:
            arc(u, sink, -balance)
    neighbors = [sorted(row) for row in residual]
    result = {"feasible": True, "interval_edges": [list(edge) for edge in edges],
              "totals": list(target), "b": balances}
    value = 0
    while value < supply:
        adjacency = [[v for v in neighbors[u] if residual[u][v] > 0]
                     for u in range(n + 3)]
        previous = _search(adjacency, source)
        if sink not in previous:
            cut = sorted(previous)
            result.update(feasible=False, supply=supply, cut=cut,
                          cut_capacity=_cut_capacity(edges, balances, supply, set(cut)))
            verify_flow_support_certificate(edges, target, result)
            return result
        path = _path(previous, sink)
        delta = min(residual[u][v] for u, v in zip(path, path[1:]))
        for u, v in zip(path, path[1:]):
            residual[u][v] -= delta
            residual[v][u] += delta
        value += delta

    flow = [supply - residual[u][v] for u, v in edges]
    arcs = set(edges) | {(v, u) for (u, v), x in zip(edges, flow) if x > 0}
    adjacency = [[] for _ in range(n + 1)]
    for u, v in sorted(arcs):
        adjacency[u].append(v)
    active, cycles, forced = [], {}, {}
    for e, ((u, v), x) in enumerate(zip(edges, flow)):
        if x > 0:
            active.append(e)
            continue
        # Every original forward edge is unbounded for this residual test,
        # even when the max-flow witness reaches the artificial supply cap.
        previous = _search(adjacency, v)
        if u in previous:
            active.append(e)
            cycles[str(e)] = _path(previous, u)
        else:
            forced[str(e)] = sorted(previous)
    components = _components(n + 1, [edges[e] for e in active])
    rank = n + 1 - components
    dimension = len(active) - rank
    result.update(flow=flow, active=active, positive_cycles=cycles,
                  forced_zero_cuts=forced, vertices_including_isolates=n + 1,
                  components=components, rank=rank, dimension=dimension,
                  degree=dimension)
    verify_flow_support_certificate(edges, target, result)
    return result


def _integer_list(value, name, minimum=None, maximum=None, length=None, unique=False):
    _require(type(value) is list, f"{name} must be a JSON array (list)")
    _require(length is None or len(value) == length, f"{name} has the wrong length")
    for i, entry in enumerate(value):
        _integer(entry, f"{name}[{i}]", minimum, maximum)
    _require(not unique or len(value) == len(set(value)), f"{name} contains duplicates")
    return value


def _mapping_keys(value, keys, name):
    _require(type(value) is dict, f"{name} must be a JSON object (dict)")
    _require(all(type(key) is str for key in value), f"{name} keys must be strings")
    _require(set(value) == set(keys), f"{name} has missing or unexpected identities/fields")


def verify_flow_support_certificate(interval_edges, totals, certificate):
    """Check a complete certificate, returning True or raising ValueError.

    True means the certificate is valid, including a valid infeasibility
    certificate; inspect its exact boolean ``feasible`` field for feasibility.
    Inputs follow flow_support_certificate's contract. The certificate must
    have exactly the documented fields and plain JSON containers. Numeric
    fields require exact Python ints, never bool or numeric coercion.

    Checks bind the original ordered edge identities and totals, verify a
    flow or strict cut inequality, require the complete disjoint active and
    forced-zero partition and all required witnesses, and independently
    compute interval-matrix rank by rational elimination. A residual path must
    be simple, so its unit augmentation proves positivity of that edge.
    Generation and max flow are not rerun. Nothing is mutated.
    """
    edges, target = _inputs(interval_edges, totals)
    n, edge_count = len(target), len(edges)
    c = certificate
    _require(type(c) is dict, "certificate must be a JSON object (dict)")
    _require(type(c.get("feasible")) is bool, "feasible must be an exact bool")
    keys = {"feasible", "interval_edges", "totals", "b"}
    if c["feasible"]:
        keys.update({"flow", "active", "positive_cycles", "forced_zero_cuts",
                     "vertices_including_isolates", "components", "rank",
                     "dimension", "degree"})
    else:
        keys.update({"supply", "cut", "cut_capacity"})
    _mapping_keys(c, keys, "certificate")
    _require(type(c["interval_edges"]) is list and len(c["interval_edges"]) == edge_count,
             "certificate interval_edges has the wrong structure or length")
    for e, original in enumerate(edges):
        pair = _integer_list(c["interval_edges"][e], f"interval_edges[{e}]", length=2)
        _require(tuple(pair) == original, "certificate does not match original edge identities")
    recorded = _integer_list(c["totals"], "totals", length=n)
    _require(tuple(recorded) == target, "certificate does not match original totals")
    balances = _balances(target)
    _require(_integer_list(c["b"], "b", length=n + 1) == balances,
             "certificate balances do not match original totals")

    if not c["feasible"]:
        supply = sum(max(b, 0) for b in balances)
        _require(_integer(c["supply"], "supply", 0) == supply, "incorrect total supply")
        cut = set(_integer_list(c["cut"], "cut", 0, n + 2, unique=True))
        _require(n + 1 in cut and n + 2 not in cut, "cut must separate source from sink")
        capacity = _cut_capacity(edges, balances, supply, cut)
        _require(_integer(c["cut_capacity"], "cut_capacity", 0) == capacity < supply,
                 "cut does not prove infeasibility")
        return True

    flow = _integer_list(c["flow"], "flow", 0, length=edge_count)
    reconstructed = tuple(sum(x for (u, v), x in zip(edges, flow) if u <= i < v)
                          for i in range(n))
    _require(reconstructed == target, "flow does not satisfy the original interval equations")
    active = _integer_list(c["active"], "active", 0, edge_count - 1, unique=True)
    active_set = set(active)
    forced = set(range(edge_count)) - active_set
    zero_active = {e for e in active if flow[e] == 0}
    _mapping_keys(c["positive_cycles"], {str(e) for e in zero_active}, "positive_cycles")
    _mapping_keys(c["forced_zero_cuts"], {str(e) for e in forced}, "forced_zero_cuts")
    arcs = set(edges) | {(v, u) for (u, v), x in zip(edges, flow) if x > 0}
    for e in zero_active:
        path = _integer_list(c["positive_cycles"][str(e)], f"positive_cycles[{e}]",
                             0, n, unique=True)
        u, v = edges[e]
        _require(len(path) >= 2 and path[0] == v and path[-1] == u,
                 f"positive_cycles[{e}] has incorrect endpoints")
        _require(all((a, b) in arcs for a, b in zip(path, path[1:])),
                 f"positive_cycles[{e}] uses a nonexistent residual arc")
    for e in forced:
        u, v = edges[e]
        cut = set(_integer_list(c["forced_zero_cuts"][str(e)], f"forced_zero_cuts[{e}]",
                                0, n, unique=True))
        _require(flow[e] == 0 and v in cut and u not in cut,
                 f"forced_zero_cuts[{e}] does not separate a zero edge")
        _require(not any(a in cut and b not in cut for a, b in arcs),
                 f"forced_zero_cuts[{e}] is not closed under residual arcs")
        _require(sum(balances[v] for v in cut) == 0,
                 f"forced_zero_cuts[{e}] has nonzero balance")

    active_edges = [edges[e] for e in active]
    components = _components(n + 1, active_edges)
    rank = _interval_rank(n, active_edges)
    _require(_integer(c["vertices_including_isolates"], "vertices_including_isolates", 1)
             == n + 1, "incorrect vertex count")
    _require(_integer(c["components"], "components", 1) == components,
             "incorrect component count including isolates")
    _require(_integer(c["rank"], "rank", 0) == rank == n + 1 - components,
             "incorrect interval/incidence rank")
    dimension = len(active) - rank
    _require(_integer(c["dimension"], "dimension", 0) == dimension,
             "incorrect intrinsic dimension")
    _require(_integer(c["degree"], "degree", 0) == dimension,
             "incorrect Ehrhart degree")
    return True
