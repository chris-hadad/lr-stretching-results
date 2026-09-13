"""Read-only consistency of the complete recorded rank-eight certificate.

This evaluates the supplied polynomial against preserved observations. It does
not run an independent tableau/column counter or establish the geometric proof.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def integer(value):
    require(type(value) is int and value >= 0, "expected nonnegative JSON integer")
    return value

def decimal(value):
    require(isinstance(value, str) and re.fullmatch(r"0|[1-9][0-9]*", value) is not None,
            "expected nonnegative decimal count string")
    return int(value)

def unique_rows(rows, key, expected, label):
    require(isinstance(rows, list), label + ": rows must be a list")
    result = {}
    for row in rows:
        identity = key(row)
        require(identity not in result, label + ": duplicate identity " + repr(identity))
        result[identity] = row
    require(set(result) == set(expected), label + ": omitted or unexpected identities")
    return result

def uv_grid(degree):
    integer(degree)
    return {(u, v) for u in range(degree+1) for v in range(degree+1-u)}

def check_grid(primary, independent, count, degree):
    """Reusable roster checker; tests use only a degree-one synthetic model."""
    expected = uv_grid(degree)
    source = unique_rows(primary, lambda r: (integer(r["u"]), integer(r["v"])),
                         expected, "primary grid")
    paired_expected = {(u+v, u+2*v) for u, v in expected}
    observed = check_paired(independent, paired_expected, count)
    for (u, v), row in source.items():
        m, s = u+v, u+2*v
        require((integer(row["M"]), integer(row["S"])) == (m, s),
                "primary grid parameter substitution mismatch")
        actual = integer(row["actual"])
        require(actual == count(m, s) == observed[m, s], "primary/paired/evaluator mismatch")
    return source

def check_paired(data, expected, count):
    require(type(data.get("schema_version")) is int and data["schema_version"] == 1
            and data.get("status") == "complete",
            "incomplete or unsupported independent model envelope")
    rows = unique_rows(data.get("cases"), lambda r: (integer(r["m"]), integer(r["s"])),
                       expected, "independent model")
    require(data.get("case_count") == len(expected) and
            data.get("completed_cases") == len(expected), "independent envelope population differs")
    result = {}
    for ordinal, row in enumerate(data["cases"]):
        identity = row["m"], row["s"]
        require(type(row.get("index")) is int and row["index"] == ordinal,
                "independent ordinal differs")
        require(row.get("status") == "complete" and type(row.get("returncode")) is int
                and row["returncode"] == 0, "refused or failed independent row")
        require(row.get("request") == {"m": identity[0], "s": identity[1]},
                "independent raw request mismatch")
        raw = row.get("result", {})
        require(type(raw.get("schema_version")) is int and raw["schema_version"] == 1
                and raw.get("status") == "complete",
                "incomplete raw independent result")
        require((integer(raw.get("m")), integer(raw.get("s"))) == identity,
                "raw independent result parameter mismatch")
        observed = decimal(row.get("count"))
        require(decimal(raw.get("count")) == observed == count(*identity),
                "independent raw/evaluator count mismatch")
        result[identity] = observed
    return result

def verify_source_map(root):
    """No lookup of historical sources: pin the supplied standalone bytes."""
    manifest = json.loads((root / "SOURCE-UPDATE.json").read_text())
    require(manifest.get("schema") == "tooling-source-update-v1", "source map schema differs")
    entries = {}
    for entry in manifest.get("files", []):
        rel = entry.get("path")
        require(isinstance(rel, str) and rel and "\\" not in rel, "invalid source-map path")
        p = Path(rel)
        require(not p.is_absolute() and ".." not in p.parts and p.as_posix() == rel,
                "source-map path traversal or normalization")
        require(rel not in entries, "duplicate source-map identity")
        path = root / p
        require(path.is_file() and not path.is_symlink()
                and root.resolve() in path.resolve().parents, "missing/nonlocal mapped file")
        raw = path.read_bytes()
        require(len(raw) == entry.get("bytes") and
                hashlib.sha256(raw).hexdigest() == entry.get("sha256"),
                "stale or changed source-map member: " + rel)
        entries[rel] = entry
    require(entries, "empty source map")
    actual = {path.relative_to(root).as_posix() for path in root.rglob("*")
              if path.is_file() and path.name != "SOURCE-UPDATE.json"
              and "__pycache__" not in path.parts}
    require(actual == set(entries), "unmapped or missing standalone file")
    return entries

def projection(root, name, entries):
    rel = "proofs/data/" + name + ".json"
    require(rel in entries, "projection not in source map")
    raw = (root / rel).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == entries[rel]["sha256"],
            "projection changed during check")
    data = json.loads(raw)
    require(data.get("schema") == "tooling-rank8-source-projection-v1",
            "unsupported projection schema")
    origin = entries[rel].get("origin", {})
    require(data.get("source_sha256") == origin.get("source_sha256"),
            "projection original-source pin differs")
    require(data.get("source_name") == Path(origin.get("source", "")).name,
            "projection original-source identity differs")
    require(isinstance(data.get("data"), dict), "projection missing mathematical data")
    return data["data"]

def main():
    entries = verify_source_map(HERE)
    from slr_ehrhart import rank8_clipped as api
    from slr_ehrhart import _rank8_clipped_data as fixed
    source = projection(HERE, "rank8-bivariate", entries)
    require(fixed.SOURCE_SHA256 == entries["proofs/data/rank8-bivariate.json"]
            ["origin"]["source_sha256"], "runtime table source certificate pin differs")
    require(source.get("status") == "complete" and source.get("total_degree_bound") == 21,
            "bivariate source incomplete or wrong degree")
    coefficients = unique_rows(source.get("ordinary_coefficients"),
                               lambda r: tuple(integer(x) for x in r["powers"]),
                               uv_grid(21), "coefficient grid")
    table_rows = [[i, j, n] for i, j, n in fixed.NUMERATOR_TERMS]
    table = unique_rows(table_rows, lambda row: tuple(row[:2]), uv_grid(21), "runtime table")
    for identity, row in coefficients.items():
        value = Fraction(row["coefficient"])
        require(value == Fraction(table[identity][2], fixed.DENOMINATOR),
                "source/runtime coefficient mismatch")
        require(value > 0, "ordinary-negative or zero mixed coefficient: " + repr(identity))
    primary = check_grid(source.get("counts"),
                         projection(HERE, "rank8-independent-grid", entries),
                         api.rank8_clipped_count, 21)
    holds = {(22, 44), (23, 46), (22, 34), (24, 31)}
    require(not holds.intersection({(u+v, u+2*v) for u, v in primary}),
            "holdouts overlap determining grid")
    held = check_paired(projection(HERE, "rank8-independent-holdouts", entries),
                        holds, api.rank8_clipped_count)
    cert = projection(HERE, "rank8-certificate", entries)
    require(cert.get("status") == "complete", "incomplete certificate")
    case = cert["case"]
    require((case.get("M"), case.get("S")) == (1, 2), "certificate boundary identity differs")
    require(tuple(tuple(case[key]) for key in ("lambda", "mu", "nu")) ==
            api.rank8_clipped_boundary(1, 2), "literal certificate boundary mismatch")
    vector = tuple(Fraction(x) for x in cert["independent_rank8_vector"])
    require(len(vector) == 22 and vector == api.rank8_clipped_polynomial(1, 2),
            "complete independent ordinary vector differs")
    held_cert = unique_rows(cert["unused_positive_holdouts"],
                            lambda row: (row["m"], row["s"]), holds, "certificate holds")
    for identity, row in held_cert.items():
        require(integer(row["count"]) == held[identity], "certificate hold mismatch")
    expected_sites = {(1, 1, t) for t in range(4)}
    expected_sites |= {(1, 2, t) for t in range(5)}
    expected_sites |= {(2, 3, t) for t in range(3)}
    sites = unique_rows(cert["literal_sites"], lambda row: tuple(row[:3]),
                        expected_sites, "literal scalar sites")
    for identity, row in sites.items():
        require(len(row) == 4 and integer(row[3]) == api.rank8_clipped_count(*identity),
                "literal scalar site differs")
    controls = unique_rows(cert["bare_LR_controls"], lambda row: row["t"],
                           {1, 2}, "recorded bare LR controls")
    for t, row in controls.items():
        require(integer(row["actual"]) == api.rank8_clipped_count(1, 2, t),
                "recorded bare LR control differs")
    # Rebind every included source after the read/evaluation sequence.
    require(entries == verify_source_map(HERE), "source map changed during check")
    print(json.dumps({
        "status": "complete",
        "scope": "recorded mathematical data consistency; no fresh LR recount or geometry proof",
        "coefficient_identities": len(coefficients), "determining_identities": len(primary),
        "unused_identities": len(held), "ordinary_vector_length": len(vector),
        "literal_sites": len(sites), "bare_LR_controls": len(controls),
    }, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
