"""Tiny self-authored fixtures only. No returned corpus or counters are run."""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations
import json
from math import prod
from pathlib import Path
import tempfile
import unittest

import verify_pro027_masks as V


def mul(a,b,degree):
    out = [Q(0)]*(degree+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j <= degree:
                out[i+j] += x*y
    return out


def orthant_trace(d):
    """Independent closed-form orthant trace, not a call to the replay engine."""
    eye = [[int(i == j) for j in range(d)] for i in range(d)]
    xi = list(range(1,d+1))
    faces = []
    for size in range(d):
        for face in combinations(range(d),size):
            rest = [i for i in range(d) if i not in face]
            q = len(rest)
            values = [Q(xi[i]) for i in rest]
            scaled = [Q(1)]+[Q(0)]*d
            regular = [Q(1)]+[Q(0)]*(d-q)
            for a in values:
                scaled = mul(scaled,[-1/a,Q(1,2),-a/12,Q(0),a**3/720],d)
                regular = mul(regular,[Q(1,2),-a/12,Q(0),a**3/720],d-q)
            mu = {str(k):"0" for k in range(-q,d-q+1)}
            mu.update({str(k):str(x) for k,x in enumerate(regular)})
            subtractions = []
            for length in range(1,q+1):
                for local in combinations(range(q),length):
                    subtractions.append({"local_face":list(local),
                        "global_face":sorted((*face,*(rest[j] for j in local))),"index":1,
                        "integral_prefactor":str(Q((-1)**length)/prod(values[j] for j in local))})
            faces.append({"face":list(face),"quotient_basis":[[int(i == j) for j in rest] for i in range(d)],
                          "quotient_metric":[[int(i == j) for j in range(q)] for i in range(q)],
                          "projected_rays":[[int(i == j) for j in range(q)] for i in range(q)],
                          "covector":list(map(str,values)),"fundamental_points":[[0]*q],
                          "S_series":{str(k-q):str(x) for k,x in enumerate(scaled)},
                          "face_subtractions":subtractions,"mu_series":mu})
    return {"tangent_rays":eye,"metric":eye,"generic_covector":xi,"faces":faces,
            "alpha":str(Q(1,2**d))}


def orthant_type(q=3):
    return {"type_id":0,"normal_index":1,
            "representative_normals":[[int(i == j) for j in range(5)] for i in range(q)],
            "normal_gram":[[int(i == j) for j in range(q)] for i in range(q)],
            "generator_permutation":list(range(q)),"alpha":str(Q(1,2**q)),
            "full_laurent":orthant_trace(q)}


def compact_orthant():
    return {"normal_rows":[[1,0,0,0],[0,1,0,0],[0,0,1,0]],
            "primitive_edge_direction":[0,0,0,1],
            "saturated_normal_basis":[["1","0","0"],["0","1","0"],["0","0","1"],["0","0","0"]],
            "integer_normal_coordinates":[["1","0","0"],["0","1","0"],["0","0","1"]],
            "primitive_tangent_rays":[[1,0,0],[0,1,0],[0,0,1]],"tangent_lattice_index":1,
            "fundamental_points":[["0","0","0"]],"generic_covector":["1","2","3"],
            "cone_laurent_constant":"11/24","complete_edge_subtraction":"1/3","alpha":"1/8",
            "facet_indices":[1,1,1]}


def small_boundary():
    # n=4 has three original variables. No accepted forcing is asserted in this
    # toy premise: the full chart is the identity, so every row must survive.
    n,d = 4,3
    rows = V.original_rows(n)
    normals = sorted({V.N.primitive(row[3*n:]) for row in rows if any(row[3*n:])})
    rec = {"rank":n,"mask":0,"symbolic_chart":{"closed":0,"free":[0,1,2],
           "offset_matrix":[[0]*(3*n) for _ in range(d)],
           "basis_rows":[[int(i == j) for j in range(d)] for i in range(d)],
           "rows":[list(row) for row in rows]},
           "reduction":{"steps":[],"kept":list(range(len(rows))),"normals":[list(row) for row in normals]}}
    return rec,{"mask":0,"closed_rows_mask":0,"dimension_bound":d}


class ExactArithmeticTests(unittest.TestCase):
    def test_exact_integer_fields_reject_fractional_and_bool(self):
        for bad in (True,False,0.5,1.0,"0.5","1.0"):
            with self.subTest(bad=bad), self.assertRaises(V.N.CheckError):
                V.exact_int(bad,text_ok=True)
        self.assertEqual(V.exact_int("-2",True),-2)

    def test_affine_implication_uses_every_coordinate(self):
        V.verify_implication((5,2,-1),((3,1,0),(2,1,-1)),(),[[0,"1"],[1,"1"]],[])
        with self.assertRaisesRegex(V.N.CheckError,"affine implication"):
            V.verify_implication((0,2,-1),((3,1,0),(2,1,-1)),(),[[0,"1"],[1,"1"]],[])
        with self.assertRaisesRegex(V.N.CheckError,"Dropped boundary"):
            V.verify_implication((5,2,-1),((2,-1),),(),[[0,"1"]],[])

    def test_affine_implication_rejects_bad_coefficients(self):
        for terms in ([[0,"-1"]],[[0,"1"],[0,"1"]],[[True,"1"]],[[0,0.5]]):
            with self.subTest(terms=terms), self.assertRaises(V.N.CheckError):
                V.verify_implication((1,2),((1,2),),(),terms,[])

    def test_exact_unrestricted_boundary_relation(self):
        V.verify_implication((1,0,0),((0,1,0),),((1,-1,0),),[[0,"1"]],[[0,"1"]])
        with self.assertRaises(V.N.CheckError):
            V.verify_implication((1,0,1),((0,1,0),),((1,-1,0),),[[0,"1"]],[[0,"1"]])


class ChartTests(unittest.TestCase):
    def test_complete_original_rhombi_by_independent_parallelograms(self):
        # Enumerate the three geometric orientations by 60-degree side pairs,
        # independently of the up/down stencil's construction and row order.
        for n in (2,3,4):
            pts = {(i,j) for i in range(n+1) for j in range(n+1-i)}
            directions = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
            cells = set()
            for p in pts:
                for a,b in combinations(directions,2):
                    if 2*a[0]*b[0]+a[0]*b[1]+a[1]*b[0]+2*a[1]*b[1] != 1:
                        continue
                    x,y,z = (p[0]+a[0],p[1]+a[1]),(p[0]+b[0],p[1]+b[1]),(p[0]+a[0]+b[0],p[1]+a[1]+b[1])
                    if {x,y,z} <= pts:
                        cells.add(tuple(sorted(((p,-1),(x,1),(y,1),(z,-1)))))
            self.assertEqual(len(cells),3*n*(n-1)//2)
            self.assertEqual(len(V.original_rows(n)),len(cells))
            # Bind actual boundary coefficients, not merely the number of cells.
            interior = sorted(p for p in pts if min(p)>0 and sum(p)<n)
            values = {}
            for i,j in pts:
                v = [0]*(3*n+len(interior))
                if (i,j) in interior:
                    v[3*n+interior.index((i,j))]=1
                else:
                    indices = list(range(n,n+i)) if j == 0 else list(range(j)) if i == 0 else list(range(n,2*n))+list(range(2*n,2*n+j))
                    for k in indices:
                        v[k] += 1
                values[i,j] = v
            wanted = sorted(tuple(sum(sign*values[p][k] for p,sign in c) for k in range(len(next(iter(values.values()))))) for c in cells)
            self.assertEqual(sorted(V.original_rows(n)),wanted)

    def test_identity_chart_complete_and_stale_geometry(self):
        rec,accepted = small_boundary()
        result = V.verify_boundary(rec,accepted,3,V.N.Deadline())
        self.assertEqual(result["original_rhombi"],18)
        self.assertEqual(result["actual_degree"],"not inferred from coordinate bound")
        accepted["dimension_bound"] = 2
        with self.assertRaisesRegex(V.N.CheckError,"Stale accepted"):
            V.verify_boundary(rec,accepted,3,V.N.Deadline())

    def test_chart_omission_and_dropped_boundary_term(self):
        for mutation in ("omit","boundary","selection"):
            rec,accepted = small_boundary()
            if mutation == "omit":
                rec["symbolic_chart"]["rows"].pop()
            elif mutation == "boundary":
                rec["symbolic_chart"]["rows"][0][0] += 1
            else:
                rec["symbolic_chart"]["basis_rows"][0][0] = 0
            with self.subTest(mutation=mutation), self.assertRaises(V.N.CheckError):
                V.verify_boundary(rec,accepted,3,V.N.Deadline())

    def test_sequential_removal_cannot_use_future_or_absent_row(self):
        rec,accepted = small_boundary()
        rec["reduction"]["steps"] = [{"removed":50,"others":[],"certificate":{"nonnegative":[],"equalities":[]}}]
        with self.assertRaisesRegex(V.N.CheckError,"absent"):
            V.verify_boundary(rec,accepted,3,V.N.Deadline())

    def test_chart_preserves_boundary_only_consistency(self):
        # Forced x0=-b0 and x0=b1 leave the consistency equation b0+b1=0.
        # The chart is valid on every nonempty fiber, although that equation is
        # not an identity on unrestricted boundaries. It must remain a row.
        raw = ((1,0,1,0),(0,1,-1,0))
        off,base,free = ((-1,0),(0,0)),((0,),(1,)),(1,)
        V.verify_chart_affine_hull(raw,off,base,free,3,())
        with self.assertRaisesRegex(V.N.CheckError,"Chart identity"):
            V.verify_chart_affine_hull(raw,((-2,0),(0,0)),base,free,3,())

    def test_whole_polynomial_bridge_uses_actual_dimension(self):
        bridge = V.whole_polynomial_bridge(5)
        full = bridge["by_actual_degree"][5]["coefficients"]
        self.assertIn("short-normal",full["3"])
        self.assertIn("normal-cycle",full["1"])
        self.assertIn("normal-cycle",full["2"])
        self.assertIn("intrinsic",full["4"])
        hidden = bridge["by_actual_degree"][4]["coefficients"]
        self.assertIn("normal-cycle",hidden["2"])
        self.assertIn("intrinsic",hidden["3"])
        four = V.whole_polynomial_bridge(4)
        self.assertIn("hidden-stratum",four["by_actual_degree"][3]["coefficients"]["1"])
        self.assertIn("short-normal",four["by_actual_degree"][4]["coefficients"]["2"])


class LaurentTests(unittest.TestCase):
    def test_complete_orthant_traces(self):
        for q in (3,4):
            result = V.verify_complete_type(orthant_type(q),"p07",V.N.Deadline())
            self.assertEqual(Q(result["alpha"]),Q(1,2**q))
            self.assertEqual(result["proper_faces"],2**q-1)
            self.assertEqual(result["fundamental_points"],2**q-1)

    def test_p08_auxiliary_lower_dimensional_traces_are_not_omitted(self):
        for q in (1,2):
            rec = orthant_type(q)
            rec["kind"] = "saturated_gram"
            rec["dimension"] = q
            rec["representative_generator_permutation"] = rec.pop("generator_permutation")
            rec["payload"] = [rec["kind"],rec["normal_gram"]]
            rec["key"] = V.N.digest(json.dumps(rec["payload"],separators=(",",":")).encode())
            result = V.verify_complete_type(rec,"p08",V.N.Deadline())
            self.assertEqual(result["proper_faces"],(1 << q)-1)
            self.assertEqual(Q(result["alpha"]),Q(1,2**q))

    def test_missing_proper_face_and_unsaturated_quotient(self):
        for mutation in ("face","quotient","point","subtraction"):
            rec = orthant_type()
            trace = rec["full_laurent"]
            if mutation == "face":
                trace["faces"].pop()
            elif mutation == "quotient":
                trace["faces"][0]["quotient_basis"][0][0] = 2
            elif mutation == "point":
                trace["faces"][0]["fundamental_points"] = []
            else:
                trace["faces"][0]["face_subtractions"].pop()
            with self.subTest(mutation=mutation), self.assertRaises(V.N.CheckError):
                V.verify_complete_type(rec,"p07",V.N.Deadline())

    def test_changed_type_normal_embedding(self):
        rec = orthant_type()
        binding = {"type_id":0,"normal_index":1,"generator_permutation":[0,1,2]}
        U = V.matrix(rec["representative_normals"])
        self.assertEqual(V.bind_type(U,binding,rec,"p07"),Q(1,8))
        changed = ((1,1,0,0,0),U[1],U[2])
        with self.assertRaisesRegex(V.N.CheckError,"Gram mismatch"):
            V.bind_type(changed,binding,rec,"p07")
        rec["normal_gram"][0][0] = 2
        with self.assertRaises(V.N.CheckError):
            V.verify_complete_type(rec,"p07",V.N.Deadline())

    def test_higher_index_requires_literal_or_explicit_signed_embedding(self):
        U = ((1,0,0,0,0),(1,2,0,0,0),(0,0,1,0,0))
        rep = [list(row) for row in U]
        old = {"normal_index":2,"representative_normals":rep,"alpha":"1/8"}
        binding = {"normal_index":2}
        self.assertEqual(V.bind_type(U,binding,old,"p07"),Q(1,8))
        changed = tuple(tuple(-x if j == 0 else x for j,x in enumerate(row)) for row in U)
        with self.assertRaisesRegex(V.N.CheckError,"literal normal embedding"):
            V.bind_type(changed,binding,old,"p07")
        payload = ["signed_ambient",rep]
        new = {**old,"kind":"signed_ambient","canonical_normals":rep,"dimension":3,"payload":payload,
               "key":V.N.digest(json.dumps(payload,separators=(",",":")).encode())}
        binding = {"normal_index":2,"generator_permutation":[0,1,2],"coordinate_permutation":list(range(5)),"coordinate_signs":[1]*5}
        self.assertEqual(V.bind_type(U,binding,new,"p08"),Q(1,8))
        binding["coordinate_signs"][0] = -1
        with self.assertRaisesRegex(V.N.CheckError,"signed integer embedding"):
            V.bind_type(U,binding,new,"p08")
        new["kind"] = "saturated_gram"
        new["normal_gram"] = [[1,0,0],[0,1,0],[0,0,1]]
        with self.assertRaises(V.N.CheckError):
            V.type_metadata(new,"p08")

    def test_compact_three_formula_rebuilt(self):
        result = V.verify_compact_three(compact_orthant(),V.N.Deadline())
        self.assertEqual(result["alpha"],"1/8")
        self.assertEqual(result["edge_subtractions"],3)

    def test_compact_omissions_scalar_and_lattice_fail(self):
        for mutation in ("points","basis","edge","facet","coordinate","scalar"):
            rec = compact_orthant()
            if mutation == "points": rec["fundamental_points"] = []
            elif mutation == "basis": rec["saturated_normal_basis"][0][0] = "2"
            elif mutation == "edge": rec["complete_edge_subtraction"] = "0"
            elif mutation == "facet": rec["facet_indices"].pop()
            elif mutation == "coordinate": rec["integer_normal_coordinates"][0][0] = "1.0"
            else: rec["alpha"] = "7/8"
            with self.subTest(mutation=mutation), self.assertRaises(V.N.CheckError):
                V.verify_compact_three(rec,V.N.Deadline())


class CorrectionTests(unittest.TestCase):
    @staticmethod
    def data():
        normals = ((1,0,0,0,0),(0,1,0,0,0),(0,0,1,0,0),(0,0,0,1,0))
        certificate = {"correction":{"status":"EXACT_STRICT","supports":[{"normals":[0,1,2],
                        "saturated_kernel_columns":[[0,0],[0,0],[0,0],[1,0],[0,1]]}],
                        "coefficients":["1/8","0"],"nonzero_support_count":1,"used_support_ids":[0]}}
        return normals,certificate

    def test_primitive_incidence_includes_positive_raw_cones(self):
        normals,certificate = self.data()
        supports = V.correction_supports(certificate,normals,1)
        value,events = V.apply_correction(normals,(0,1,2,3),Q(1,16),supports)
        self.assertEqual(value,Q(3,16))
        self.assertEqual(events,[{"support":0,"extra":3,"primitive_quotient":[1,0]}])
        self.assertEqual(V.apply_correction(normals,(0,1,2,3),Q(1,16),{})[0],Q(1,16))

    def test_primitive_divisor_uses_all_kernel_coordinates(self):
        normals,certificate = self.data()
        normals = normals[:3]+((1,0,0,2,3),)
        supports = V.correction_supports(certificate,normals,1)
        value,events = V.apply_correction(normals,(0,1,2,3),Q(0),supports)
        self.assertEqual(events[0]["primitive_quotient"],[2,3])
        self.assertEqual(value,Q(1,4))

    def test_dropped_or_unsaturated_support_fails(self):
        for mutation in ("kernel","coefficient","duplicate","identity"):
            normals,c = self.data()
            co = c["correction"]
            if mutation == "kernel": co["supports"][0]["saturated_kernel_columns"][3][0] = 2
            elif mutation == "coefficient": co["coefficients"].pop()
            elif mutation == "duplicate":
                co["supports"].append(deepcopy(co["supports"][0]));co["coefficients"] *= 2
            else: co["supports"][0]["normals"] = [0,0,2]
            with self.subTest(mutation=mutation), self.assertRaises(V.N.CheckError):
                V.correction_supports(c,normals,1)

    def test_raw_and_corrected_negative_are_preserved_as_local_only(self):
        row = V.preserve_local_result(Q(-1,7),Q(-1,11),[])
        self.assertEqual(row["raw"],"-1/7")
        self.assertEqual(row["corrected"],"-1/11")
        self.assertFalse(row["strictly_positive"])
        self.assertTrue(row["raw_negative"])
        self.assertIn("not a whole LR coefficient",row["scope"])


def toy_cone_work(with_correction=False):
    """Five orthogonal normals: every 3/4 subset is independent and raw positive."""
    normals = sorted([[int(i == j) for j in range(5)] for i in range(5)])
    types = [orthant_type(3),orthant_type(4)]
    types[1]["type_id"] = 1
    certificates = []
    for coefficient in (1,2):
        q = 5-coefficient
        cones = [list(row) for row in combinations(range(5),q)]
        co = {"status":"ALREADY_STRICT","supports":[],"coefficients":[],
              "nonzero_support_count":0,"minimum":str(Q(1,2**q))}
        if with_correction and coefficient == 1:
            co = {"status":"EXACT_STRICT","supports":[{"normals":[0,1,2],
                  "saturated_kernel_columns":[[1,0],[0,1],[0,0],[0,0],[0,0]]}],
                  "coefficients":["1/8","1/8"],"nonzero_support_count":1,"used_support_ids":[0],
                  "minimum":"1/16","incidence":[],"corrected_values":[]}
            for row in cones:
                affected = {0,1,2} <= set(row)
                if affected:
                    extra = next(i for i in row if i not in (0,1,2))
                    co["incidence"].append([{"support":0,"extra":extra,"primitive_quotient":[int(extra == 4),int(extra == 3)]}])
                else:
                    co["incidence"].append([])
                co["corrected_values"].append("3/16" if affected else "1/16")
        certificates.append({"coefficient":coefficient,"cones":cones,
                             "alphas":[str(Q(1,2**q))]*len(cones),
                             "type_bindings":[{"type_id":int(q == 4),"normal_index":1,"generator_permutation":list(range(q))} for _ in cones],
                             "negative_cones":0,"zero_cones":0,"uncorrected_minimum":str(Q(1,2**q)),"correction":co})
    boundary = {"rank":6,"mask":43,"reduction":{"normals":normals}}
    cycle = {"rank":6,"mask":43,"normals":normals,"certificates":certificates}
    class ToySources:
        def read(self,key):
            return {"packet:boundary":[boundary],"packet:cycle":[cycle],"packet:types":types}[key]
    manifest = {"stage":"p07","presentations":[{"id":"6:43","rank":6,"mask":43,"dimension":5,"normal_count":5,
                                                "boundary":V.source_ref("packet:boundary",0),"cycle":V.source_ref("packet:cycle",0)}],
                "types":[{"id":f"p07:T{i}","ref":V.source_ref("packet:types",i)} for i in range(2)]}
    obligation = {"id":"cones/6:43/c1","kind":"cones","presentation":"6:43","coefficient":1,"q":4,"total":5,
                  "targets":{"independent":5}}
    return V.Work(manifest,ToySources(),V.N.Deadline()),obligation,cycle


class CompleteConeTests(unittest.TestCase):
    def test_complete_independent_subset_roster_and_type_bindings(self):
        work,obligation,_ = toy_cone_work()
        result = {}
        V.run_slice(work,obligation,0,5,result)
        self.assertEqual(result["status"],"OBLIGATION_VERIFIED")
        self.assertEqual(len(result["records"]),5)
        self.assertTrue(all(row["independent"] and row["strictly_positive"] for row in result["records"]))

    def test_missing_positive_cone_is_not_just_a_smaller_source_count(self):
        work,obligation,cycle = toy_cone_work()
        for key in ("cones","alphas","type_bindings"):
            cycle["certificates"][0][key].pop(0)
        # Even an internally consistent smaller claimed count must not omit the
        # first independent candidate from complete ambient subset enumeration.
        obligation["targets"]["independent"] = 4
        with self.assertRaisesRegex(V.N.CheckError,"Omitted independent subset"):
            work.cone(obligation,0)

    def test_duplicate_cone_or_missing_coefficient_roster_fails(self):
        for mutation in ("duplicate","coefficient"):
            work,obligation,cycle = toy_cone_work()
            if mutation == "duplicate":
                cycle["certificates"][0]["cones"][1] = cycle["certificates"][0]["cones"][0]
            else:
                cycle["certificates"].pop()
            with self.subTest(mutation=mutation), self.assertRaises(V.N.CheckError):
                work.cone(obligation,0)

    def test_missing_incidence_for_raw_positive_cone_fails(self):
        work,obligation,cycle = toy_cone_work(True)
        self.assertEqual(work.cone(obligation,0)["corrected"],"3/16")
        work,obligation,cycle = toy_cone_work(True)
        cycle["certificates"][0]["correction"]["incidence"][0] = []
        with self.assertRaisesRegex(V.N.CheckError,"primitive incidence"):
            work.cone(obligation,0)


class CoverageTests(unittest.TestCase):
    def test_complete_missing_overlap_and_duplicate_intervals(self):
        self.assertEqual(V.complete_intervals([(2,4),(0,2)],4),[])
        self.assertEqual(V.complete_intervals([(0,1),(2,3)],4),[[1,2],[3,4]])
        for chunks in ([(0,2),(1,4)],[(0,4),(0,4)],[(0,0)]):
            with self.subTest(chunks=chunks), self.assertRaises(V.N.CheckError):
                V.complete_intervals(chunks,4)

    def test_stale_missing_and_duplicate_source_ids(self):
        for records in ([{"id":0}],[{"id":0},{"id":0}],[{"id":0},{"id":2}]):
            with self.subTest(records=records), self.assertRaises(V.N.CheckError):
                V.unique_map(records,lambda r:r["id"],(0,1))

    def test_exact_mask_word_identity_and_float_rejection(self):
        for mask in (0,1,9,37):
            images = list(V.words(mask,3))
            self.assertEqual(len(images),12)
            self.assertIn(mask,{m for m,_ in images})
        self.assertEqual(V.apply_word(37,3,{"dual":0,"outer":2,"inners":[0,1]}),37)
        with self.assertRaises(V.N.CheckError):
            V.apply_word(37,3,{"dual":0.5,"outer":2,"inners":[0,1]})

    def test_member_roster_overlap_rejected(self):
        with self.assertRaises(V.N.CheckError):
            V.member_map([{"rank":3,"mask":1,"members":[1,2]},
                          {"rank":3,"mask":2,"members":[2,3]}],5)

    def test_freeze_binding_detects_changed_bytes_and_duplicate_json(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/"data.json"
            p.write_text('{"one":1}')
            sources = V.Sources(td)
            self.assertEqual(sources.read("packet:data.json"),{"one":1})
            p.write_text('{"one":2}')
            with self.assertRaisesRegex(V.N.CheckError,"changed during"):
                sources.unchanged()
            with self.assertRaises(V.N.CheckError):
                V.N.decode('{"one":1,"one":2}')

    def test_slice_deadline_never_marks_unfinished_branch_zero(self):
        class ToyWork:
            deadline = V.N.Deadline()
            def type_job(self,ordinal):
                if ordinal == 1:
                    raise V.N.DeadlineReached()
                return {"id":"toy:0","alpha":"1/8"}
        result = {}
        V.run_slice(ToyWork(),{"id":"types","kind":"types","total":3},0,3,result)
        self.assertEqual(result["status"],"PARTIAL")
        self.assertEqual(result["next_start"],1)
        self.assertEqual(result["checked_ids"],["toy:0"])
        self.assertEqual(len(result["records"]),1)

    def test_nonpositive_slice_retains_exact_failure(self):
        class ToyWork:
            deadline = V.N.Deadline()
            def cone(self,obligation,ordinal):
                return {"id":"toy:negative",**V.preserve_local_result(Q(-1,5),Q(-1,9),[])}
        result = {}
        V.run_slice(ToyWork(),{"id":"cones/toy/c1","kind":"cones","total":1},0,1,result)
        self.assertEqual(result["status"],"FAILED")
        self.assertEqual(result["records"][0]["corrected"],"-1/9")

    def test_partial_aggregate_omission_and_stale_report(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ref = {"source":"packet:toy.json","index":0}
            manifest = {"stage":"p07","checker_versions":{"checker":"one"},"sources":{},
                        "obligations":[{"id":"types","kind":"types","total":2}],
                        "types":[{"id":"toy:0","ref":ref},{"id":"toy:1","ref":ref}],"presentations":[]}
            report = {"schema":V.SCHEMA,"kind":"slice","stage":"p07","manifest_sha256":"frozen",
                      "checker_versions":manifest["checker_versions"],"status":"PARTIAL","inputs_unchanged":True,
                      "read_inputs":{},"obligation":"types","start":0,"next_start":1,"total":2,
                      "checked_ids":["toy:0"],"records":[{"id":"toy:0","ordinal":0,"source":ref,"alpha":"1/8",
                                                                  "q":3,"fundamental_points":7,"proper_faces":7}]}
            p = root/"report.json";p.write_text(json.dumps(report))
            args = (manifest,"frozen",V.Sources(root),[p],V.N.Deadline())
            result = V.aggregate_reports(*args)
            self.assertEqual(result["status"],"PARTIAL")
            self.assertEqual(result["missing_intervals"],{"types":[[1,2]]})
            report["checker_versions"] = {"checker":"old"};p.write_text(json.dumps(report))
            with self.assertRaisesRegex(V.N.CheckError,"Stale/mixed"):
                V.aggregate_reports(*args)
            report["checker_versions"] = manifest["checker_versions"]
            report["checked_ids"] = ["toy:1"];p.write_text(json.dumps(report))
            with self.assertRaisesRegex(V.N.CheckError,"Checked identity"):
                V.aggregate_reports(*args)


if __name__ == "__main__":
    unittest.main()
