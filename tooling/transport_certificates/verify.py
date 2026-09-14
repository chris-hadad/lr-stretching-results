#!/usr/bin/env python3
"""Complete standard-library verification of transportation/capped certificates."""

import argparse, hashlib, json, sys, time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import arithmetic as a

HERE = Path(__file__).resolve().parent
CERTIFICATE_SHA256 = "23c920924ea2641fc6143ce973fde26844c1639e28491769984b3b4a28650ced"
SYSTEMS = {
    "capped_m4": (7, 13, 6, F(1, 300)),
    "transport_3x4": (6, 12, 5, F(1, 720)),
    "transport_3x5": (8, 15, 7, F(1, 1000000)),
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique(pairs):
    out = {}
    for key, value in pairs:
        a.need(key not in out, "Duplicate JSON key")
        out[key] = value
    return out


def read_certificate(path):
    body = Path(path).read_bytes()
    a.need(len(body) <= 1000000, "Certificate exceeds size bound")
    return json.loads(
        body,
        object_pairs_hook=unique,
        parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite JSON")),
    )


def write(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, sort_keys=True, separators=(",", ":"))
        stream.write("\n")


def validate_certificate(data):
    a.need(
        set(data)
        == {"schema", "systems", "fields", "field_coordinate_rule", "source_bindings"},
        "Certificate fields differ",
    )
    a.need(data["schema"] == "transport-cap-positive-fields-v1", "Certificate schema")
    a.need(set(data["systems"]) == set(SYSTEMS), "Missing or extra normal system")
    for name, (dim, count, qmax, margin) in SYSTEMS.items():
        s = data["systems"][name]
        a.need(
            set(s) == {"dimension", "normals", "qmax", "margin", "counts"},
            "System fields differ",
        )
        a.need(
            (s["dimension"], s["normals"], s["qmax"]) == (dim, count, qmax)
            and F(s["margin"]) == margin,
            "System theorem bounds differ",
        )
        a.need(len(s["counts"]) == qmax, "Missing coefficient population")
        a.need(
            all(type(v) is int and v >= 0 for row in s["counts"] for v in row),
            "Invalid population counts",
        )
        a.need(
            all(len(row) == 3 and row[0] == row[1] + row[2] for row in s["counts"]),
            "Population partition",
        )
    a.need(
        set(data["fields"]) == {"5", "6", "7"}, "Complete correction orders required"
    )
    normal_rows, _ = a.normals("transport_3x5")
    fields = {}
    for text_q, records in data["fields"].items():
        q = int(text_q)
        field = {}
        a.need(
            isinstance(records, list) and len(records) <= 5000,
            "Bounded field record list required",
        )
        for record in records:
            a.need(set(record) == {"support", "ambient"}, "Field record schema")
            ids = record["support"]
            vector = record["ambient"]
            a.need(
                isinstance(ids, list)
                and len(ids) == q - 1
                and all(type(i) is int and 0 <= i < 15 for i in ids),
                "Invalid normal support",
            )
            a.need(
                ids == sorted(set(ids)) and tuple(ids) not in field,
                "Duplicated or unsorted support",
            )
            a.need(
                isinstance(vector, list)
                and len(vector) == 8
                and all(type(x) is str and len(x) <= 256 for x in vector),
                "Invalid ambient vector",
            )
            value = tuple(F(x) for x in vector)
            a.need(any(value), "Zero field records must be omitted")
            support = tuple(tuple(normal_rows[i]) for i in ids)
            a.need(
                a.image_index(support) == 1,
                "Field support must have full primitive image lattice",
            )
            a.need(
                all(sum(F(x) * y for x, y in zip(row, value)) == 0 for row in support),
                "Field does not annihilate its support",
            )
            field[tuple(ids)] = value
        fields[q] = field
    return fields


def corrected(alpha, ids, normal_rows, field):
    result = alpha
    for i in ids:
        support = tuple(j for j in ids if j != i)
        g = field.get(support)
        if g is not None:
            result += sum(x * y for x, y in zip(g, normal_rows[i]))
    return result


def verify(data, out):
    fields = validate_certificate(data)
    cache = {}
    summaries = []
    grand_total = grand_independent = 0
    started = time.monotonic()
    for name, (dimension, count, qmax, margin) in SYSTEMS.items():
        normals, labels = a.normals(name)
        a.need(
            len(normals) == count and all(len(row) == dimension for row in normals),
            "Original normal dimensions",
        )
        a.need(len(set(map(tuple, normals))) == count, "Duplicate normal")
        for q in range(1, qmax + 1):
            stamp = f"{name}-q{q}"
            records = []
            dependent = []
            inputs = []
            seen = 0
            for ids in combinations(range(count), q):
                seen += 1
                rows = tuple(tuple(normals[i]) for i in ids)
                index = a.image_index(rows)
                if index == 0:
                    dependent.append(ids)
                    continue
                a.need(index == 1, "Image-lattice index must be one before Gram reuse")
                # Index one of the complete row map also makes every coordinate projection surjective.
                metric, order = a.canonical(a.gram(rows))
                identity = a.type_id(metric)
                if identity not in cache:
                    alpha, control = a.bv(metric)
                    cache[identity] = (alpha, control)
                alpha, control = cache[identity]
                field = fields[q] if name == "transport_3x5" and q >= 5 else {}
                beta = corrected(alpha, ids, normals, field)
                a.need(
                    beta >= margin,
                    f"Coefficient certificate failed: {stamp} {ids} {beta}",
                )
                label = "n" + "-".join(map(str, ids))
                records.append(
                    {
                        "label": label,
                        "ids": ids,
                        "index": index,
                        "type": identity,
                        "alpha": str(alpha),
                        "beta": str(beta),
                    }
                )
                inputs.append(
                    " ".join(
                        map(
                            str,
                            [
                                label,
                                q,
                                dimension,
                                index,
                                *[v for row in rows for v in row],
                            ],
                        )
                    )
                    + "\n"
                )
            counts = [seen, len(records), len(dependent)]
            a.need(
                counts == data["systems"][name]["counts"][q - 1],
                f"Incomplete original population: {stamp}",
            )
            grand_total += seen
            grand_independent += len(records)
            result = {
                "system": name,
                "q": q,
                "dimension": dimension,
                "counts": counts,
                "minimum_raw": str(min(F(x["alpha"]) for x in records)),
                "negative_raw": sum(F(x["alpha"]) < 0 for x in records),
                "minimum_corrected": str(min(F(x["beta"]) for x in records)),
                "margin": str(margin),
            }
            write(
                out / (stamp + ".json"),
                {
                    "summary": result,
                    "normals": normals,
                    "labels": labels,
                    "independent": records,
                    "dependent": dependent,
                },
            )
            (out / (stamp + ".input")).write_text("".join(inputs))
            summaries.append(result)
            print(json.dumps(result), flush=True)
    a.need(
        grand_total == 22063 and grand_independent == 16848,
        "Whole original census differs",
    )
    result = {
        "status": "PASS_COMPLETE_TRANSPORT_AND_CAPPED_CERTIFICATES",
        "all_original_subsets": grand_total,
        "independent_subsets": grand_independent,
        "dependent_subsets": grand_total - grand_independent,
        "safe_metric_types": len(cache),
        "systems": summaries,
        "seconds": time.monotonic() - started,
        "certificate_sha256": CERTIFICATE_SHA256,
        "scope": "All coefficients of every 3-by-5 transportation polytope and the stated four-capacity whole LR family; no whole-rank theorem.",
    }
    result["artifacts"] = {
        p.name: digest(p)
        for p in sorted(out.iterdir())
        if p.name not in {"START.json", "RESULT.json"}
    }
    write(out / "RESULT.json", result)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = args.out.absolute()
    a.need(
        not out.exists() and not out.is_symlink() and out.parent.is_dir(),
        "A fresh output directory with existing parent is required",
    )
    a.need(
        out != HERE and HERE not in out.parents,
        "Keep generated outputs outside source module",
    )
    a.need(
        digest(HERE / "certificate.json") == CERTIFICATE_SHA256,
        "Exact published certificate bytes differ",
    )
    data = read_certificate(HERE / "certificate.json")
    validate_certificate(data)
    out.mkdir()
    write(
        out / "START.json",
        {
            "schema": "transport-cap-verify-run-v1",
            "python": sys.version,
            "sources": {
                name: digest(HERE / name)
                for name in ["verify.py", "arithmetic.py", "certificate.json"]
            },
            "scope": "Complete original normal census, all local constants and every rational inequality",
            "children": 0,
        },
    )
    result = verify(data, out)
    print(result["status"], flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyboardInterrupt) as error:
        print("REFUSED: " + str(error), file=sys.stderr)
        raise SystemExit(2)
