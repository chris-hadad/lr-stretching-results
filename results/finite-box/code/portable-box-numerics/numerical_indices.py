"""Explicit index adapters around preserved root mathematics, without old receipts."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
import common as U


def metadata_roster(recipe, cohort, deadline, unit_filter=None):
    """Freeze literal identities; first-unused U02 also rechecks source proofs."""
    I = U.Inputs(recipe); C = U.original("portable-box-components"); R = U.original("recount_records")
    selected = U.read(recipe["metadata"]["chosen_terminals"]["path"])
    groups = []
    if cohort == "production":
        for unit, total in C.COUNTS.items():
            if unit_filter is not None and unit != unit_filter: continue
            deadline.check()
            compact = C.compact_path(unit); records = {}; raw_rows = {}
            for ordinal, z, raw in I.records(compact):
                idx = U.record_id(z); U.need(idx not in records, "Duplicate full compact ID")
                geometry = z.get("geometry", {})
                gh = z.get("geometry_sha256", geometry.get("sha256") if isinstance(geometry, dict) else None)
                records[idx] = {"id": idx, "unit": unit, "compact": compact, "source_ordinal": ordinal,
                                "compact_sha256": U.sha(raw), "geometry_sha256": gh, "bare_triple": z.get("bare_triple")}
                raw_rows[idx] = z
            U.need(len(records) == total, "Full unit compact population differs")
            streams = [s for s in recipe["geometry_streams"] if s["unit"] == unit]
            if unit == "U11": streams = [{"key": "U11/all", "unit": unit, "shard": None, "count": total}]
            seen = set()
            for stream in streams:
                if unit == "U11":
                    names = sorted({R.relative_source(z["geometry_input"],unit) for z in raw_rows.values()})
                    order = []
                    for name in names:
                        for _i, z, _raw in I.records(f"namespaces/u11/{name}"):
                            idx = U.record_id(z)
                            if idx in records and R.relative_source(raw_rows[idx]["geometry_input"],unit) == name: order.append(idx)
                else:
                    folder = f"DATA/U04/layer5-results/{stream['shard']}" if unit == "U04" else f"DATA/{unit}/production/{stream['shard']}/counts"
                    wanted = set(records) if unit == "U04" else {
                        idx for idx, z in raw_rows.items() if
                        (str(Path(R.relative_source(z['geometry']['path'],unit)).parent) if unit == 'U05'
                         else R.relative_source(z['evidence_directory'],unit)) == folder}
                    order = [U.record_id(z) for _i,z,_raw in I.records(f"namespaces/{unit.lower()}/{folder}/certificates.jsonl")
                             if U.record_id(z) in wanted]
                U.need(len(order) == stream["count"] and len(set(order)) == len(order) and not seen.intersection(order),
                       "Missing/duplicated/cross-shard production source IDs")
                seen.update(order)
                groups.append({"key": stream["key"], "unit": unit, "shard": stream["shard"], "records": [records[i] for i in order]})
            U.need(seen == set(records), "Physical stream union differs from the full unit compact")
    elif cohort in ("U02", "U03"):
        name = f"namespaces/{cohort.lower()}/{C.EARLY[cohort]}"
        rows = [(i,z,U.encoded(z)) for i,z in enumerate(I.document(name)["records"])] if cohort == "U02" else I.records(name)
        all_rows = []; seen = set()
        for ordinal,z,raw in rows:
            idx = U.record_id(z); U.need(idx not in seen,"Duplicate advertised early identity"); seen.add(idx)
            all_rows.append({"id":idx,"unit":cohort,"compact":name,"source_ordinal":ordinal,"compact_sha256":U.sha(raw),
                             "bare_triple":z["bare_triple"],"source_status":z.get("status")})
        U.need(len(all_rows) == (211 if cohort == "U02" else 4131),"Advertised early source population differs")
        ids = selected[C.EARLY_KEYS[cohort]]
        U.need(len(ids) == U.TOTALS[cohort] and len(set(ids)) == len(ids) and set(ids) <= seen,"Wrong exact used early IDs")
        groups = [{"key":cohort,"unit":cohort,"shard":None,"records":[r for r in all_rows if r["id"] in set(ids)]}]
        if cohort == 'U02' and recipe['holdouts'] == 'first-unused':
            freeze_u02_hold_roster(recipe,I,groups[0]['records'],deadline)
    else:
        P = U.original("accept_legacy_prefix")
        document = U.read(recipe["metadata"]["legacy_vectors"]["path"])
        rows = P.metadata_roster(document,selected,prefix_ids=tuple(range(297)))
        for label, part in (("legacy-prefix",rows[:272]),("legacy-tail",rows[272:])):
            groups.append({"key":label,"unit":"LEGACY","shard":None,"records":[
                {"id":r["id"],"unit":"LEGACY","terminal_id":r["terminal_id"],"bare_triple":r["bare_triple"],
                 "compact_sha256":U.sha(U.encoded(r)),"source_ordinal":r["id"],
                 "source_metadata":recipe["metadata"]["legacy_vectors"]} for r in part]})
    population = C.COUNTS[unit_filter] if cohort == "production" and unit_filter else U.TOTALS[cohort]
    U.need(sum(len(g["records"]) for g in groups) == population, "Full literal cohort roster is incomplete")
    full_groups = groups
    if recipe["mode"] == "representative":
        # One source-order representative per production unit, both legacy
        # geometries, and both advertised U03 numerical certificate kinds.
        if cohort == "production":
            seen = set(); groups = []
            for g in full_groups:
                if g["unit"] not in seen:
                    seen.add(g["unit"]); groups.append({**g,"records":g["records"][:1]})
        elif cohort == "U03":
            kinds = set(); kept = []
            for r in groups[0]["records"]:
                if r["source_status"] not in kinds: kinds.add(r["source_status"]); kept.append(r)
            groups = [{**groups[0],"records":kept}]
        else: groups = [{**g,"records":g["records"][:1]} for g in groups]
    I.after()
    return {"schema":U.SCHEMA,"kind":"roster","status":"FROZEN_LITERAL_ROSTER","cohort":cohort,
            "mode":recipe["mode"],"full_source_groups":full_groups,"selected_groups":groups,
            "unit_filter":unit_filter,"full_source_population":population,"selected_population":sum(len(g["records"]) for g in groups),
            "inputs":[*I.meta.values(),*I.used.values()],
            "source_mathematics_performed":cohort=='U02' and recipe['holdouts']=='first-unused',
            "fresh_lattice_counts_performed":False,
            "u02_holdouts":recipe['holdouts'] if cohort=='U02' else None,
            "u02_changed_parent_ids":[r['id'] for g in full_groups for r in g['records']
                                      if r.get('u02_holdout_policy',{}).get('amendment')],
            "u02_replacement_node_ids":[f"U02:{r['id']}:{n['kind']}" for g in full_groups for r in g['records']
                                      for n in r.get('u02_holdout_policy',{}).get('required_nodes',[])
                                      if n['role']=='replacement_positive_holdout']}


def configure_geometry(recipe):
    G = U.original("box_geometry"); GE = U.original("box_geometry_early")
    base = Path(recipe["data_root"]) / "namespaces/base"
    G.CANONICAL = base; GE.CANONICAL = base
    return G, GE


def u02_hold_policy(record, original_nodes, option):
    U.need(option in ('original','first-unused') and record['unit']=='U02'
           and record['status']=='PASS_CONDITIONAL_ON_RECORDED_COUNTS','U02 hold policy needs complete source verification')
    H=U.original('prepare_u02_hold_amendments')
    determining=record['determining_nodes']; grades=H.replacement_grades(determining)
    fitting=[n for n in original_nodes if n['role']=='determining']
    old=[n for n in original_nodes if n['role']=='positive_holdout']
    U.need(len(fitting)+len(old)==len(original_nodes) and len(old)==2
           and [n['grade'] for n in old]==record['unused_hold_nodes'],'Incomplete original U02 physical roster')
    U.need({('I' if t<0 else 'P')+str(abs(t)) for t in determining}=={n['kind'] for n in fitting},
           'Hold policy omitted an original determining node')
    coefficients=list(map(Fraction,record['coefficients']))
    U.need(coefficients and coefficients[0]==1 and all(v>=0 for v in coefficients),'Changed complete nonnegative source vector')
    policy={'option':option,'rule':H.RULE if option=='first-unused' else 'all original physical holds',
            'determining_nodes':determining,'geometry_sha256':record['geometry_check']['original_geometry_sha256'],
            'certificate_reference':record['certificate'],'complete_source_coefficients':record['coefficients'],
            'original_nodes':original_nodes,'required_nodes':original_nodes,'amendment':None}
    if option=='original' or grades==record['unused_hold_nodes']: return policy
    holds=[]
    for t in grades:
        value=sum(c*t**i for i,c in enumerate(coefficients))
        U.need(value.denominator==1 and value>0 and t not in determining,'Invalid new unused held expectation')
        holds.append({'kind':'P'+str(t),'grade':t,'strict':False,'stored':{'polynomial_expectation':int(value)},
                      'role':'replacement_positive_holdout'})
    policy['required_nodes']=sorted([*fitting,*holds],key=lambda n:(n['strict'],n['grade']))
    policy['amendment']={'schema':'portable-u02-exact-holdout-amendment-v1','parent_id':record['id'],'rule':H.RULE,
                        'removed_original_node_ids':[f"U02:{record['id']}:{n['kind']}" for n in old],
                        'replacement_node_ids':[f"U02:{record['id']}:{n['kind']}" for n in holds],
                        'original_holds_remain_supplemental':old,'fresh_replacement_counts_still_required':True,
                        'geometry_and_vector_preserved':{'geometry_check':record['geometry_check'],'certificate':record['certificate'],
                                                         'coefficients':record['coefficients']}}
    return policy


def freeze_u02_hold_roster(recipe,I,expected,deadline):
    """Freeze every changed parent/node before the first U02 numerical count."""
    E=U.original('verify_early_terminals'); EI=U.original('index_early_recounts'); configure_geometry(recipe)
    class Portable(E.Inputs):
        def path(self,name):
            p=I.path(name); actual=super().path(name); U.need(actual==p,'U02 portable source resolver differs'); return actual
    inputs=Portable(I.root,I.meta['source_manifest']['path'],I.meta['source_manifest']['sha256'])
    # This runs only inside the fresh bounded roster child; the path is supplied
    # by that child and cannot refer to an old science output.
    inputs.candidate_path=Path(recipe['_current_output']).with_suffix('.candidate.json')
    rows={U.record_id(z):(z,ref) for z,ref in inputs.records(expected[0]['compact'],'records')}
    try:
        for r in expected:
            deadline.check(); certificate,ref=rows[r['id']]
            U.need(ref['record_sha256']==r['compact_sha256'],'U02 source identity changed before held-rule freezing')
            inputs.candidate_context={'id':r['id'],'unit':'U02','bare_triple':certificate['bare_triple'],'certificate_source':ref}
            verified=E.verify_u02(inputs,certificate,ref); verified['status']='PASS_CONDITIONAL_ON_RECORDED_COUNTS'
            r['u02_holdout_policy']=u02_hold_policy(verified,EI.physical_nodes(verified),'first-unused')
    finally:
        inputs.finish(); I.after()


def production_index(recipe, op, output, deadline, result):
    I = U.Inputs(recipe); R = U.original("recount_records")
    unit, wanted = op["unit"], {r["id"] for r in op["records"]}
    root = I.root / "namespaces" / unit.lower()
    compact = f"DATA/{unit}/" + R.COMPACT[unit]
    OriginalSources = R.Sources
    class PortableSources(OriginalSources):
        def path(self,name):
            expected = I.path(f"namespaces/{unit.lower()}/" + U.relative(name))
            actual = super().path(name)
            U.need(actual == expected,"Production source resolver differs")
            return actual
        def records(self,name):
            for number,raw,z in super().records(name):
                if name != compact or U.record_id(z) in wanted:
                    yield number,raw,z
    # A single explicit namespace/path/selection adapter. No filesystem API or
    # mathematical predicate is patched; physical source line numbers persist.
    R.Sources = PortableSources
    args = SimpleNamespace(root=str(root),unit=unit,shard=op["shard"],input=None,
                           geometry_identities=[],output=str(output))
    try:
        R.index_jobs(args,deadline,result)
    finally:
        R.Sources = OriginalSources
        I.after()
        result["portable_accessed_sources"] = list(I.used.values())
        result["source_bytes_verified_before_after"] = True
    U.need(result["expected_record_ids"] == sorted(wanted),"Production index changed the explicit source-ID selection")


def append_job(stream, result, job):
    raw = U.encoded(job) + b"\n"; offset = stream.tell(); stream.write(raw); stream.flush()
    result["records"].append({"ordinal":len(result["records"]),"id":job["id"],"geometry_sha256":job["geometry_sha256"],
       "offset":offset,"bytes":len(raw),"sha256":U.sha(raw),"node_ids":[f"{job['unit']}:{job['id']}:{n['kind']}" for n in job["nodes"]]})


def early_index(recipe, op, output, deadline, result):
    I = U.Inputs(recipe); E = U.original("verify_early_terminals"); EI = U.original("index_early_recounts")
    configure_geometry(recipe)
    class PortableEarlyInputs(E.Inputs):
        def path(self,name):
            expected=I.path(name); actual=super().path(name)
            U.need(actual == expected,"Early source resolver differs"); return actual
    inputs = PortableEarlyInputs(I.root,I.meta['source_manifest']['path'],I.meta['source_manifest']['sha256'])
    inputs.candidate_path = output.with_suffix('.candidate.json')
    unit = op['unit']; source = op['records'][0]['compact']
    by_id = {U.record_id(z):(z,ref) for z,ref in inputs.records(source,'records' if unit=='U02' else None)}
    ledger = output.with_suffix('.early-bindings.jsonl')
    try:
        with output.with_suffix('.jobs.jsonl').open('xb') as jobs,ledger.open('xb') as evidence:
            for expected in op['records']:
                deadline.check(); idx=expected['id']; certificate,cref=by_id[idx]
                U.need(cref['record_sha256']==expected['compact_sha256'],'Early certificate source changed')
                inputs.candidate_context={'id':idx,'unit':unit,'bare_triple':certificate['bare_triple'],'certificate_source':cref}
                start_ref=len(inputs.references)
                record=E.verify_u02(inputs,certificate,cref) if unit=='U02' else E.verify_u03(inputs,certificate,cref)
                record.update(status='PASS_CONDITIONAL_ON_RECORDED_COUNTS',source_references=inputs.references[start_ref:])
                raw=U.encoded(record)+b'\n'; evidence.write(raw); evidence.flush()
                ref=record['geometry_sources'][0] if unit=='U02' else record['geometry_source']
                g,gref=inputs.get(ref['path'],idx,'records' if unit=='U02' else None)
                U.need(gref==ref and E.digest(E.encoded(g))==record['geometry_check']['original_geometry_sha256'],
                       'Newly verified early geometry binding changed')
                nodes=EI.physical_nodes(record); actual=any(n['strict'] for n in nodes)
                policy=None
                if unit=='U02':
                    policy=u02_hold_policy(record,nodes,recipe['holdouts'])
                    if recipe['holdouts']=='first-unused':
                        U.need(policy==expected['u02_holdout_policy'],'U02 policy differs from its complete frozen source/vector/geometry roster')
                    nodes=policy['required_nodes']
                U.need(not actual or record['geometry_check']['actual_dimension_proved'],'Interior needs a proved actual hull')
                adapted,binding=E.normalize_geometry(g,unit,actual)
                if actual: U.need(binding['normalized_geometry_sha256']==record['geometry_check']['normalized_geometry_sha256'],'Geometry normalization changed')
                job={'id':idx,'unit':unit,'bare_triple':g['original'],'geometry_sha256':record['geometry_check']['original_geometry_sha256'],
                     'geometry_reference':ref,'certificate_reference':cref,'model':EI.chart_model(adapted,actual),'nodes':nodes,
                     'geometry_acceptance':'FRESH_COPIED_EARLY_GEOMETRY_AND_SOURCE_BINDING',
                     'source_binding_record':{'path':str(ledger),'line':len(result['records'])+1,'sha256':U.sha(raw)},
                     'source_refusals_preserved':sum(b['status']!='complete' for b in record['count_bindings'])}
                if policy is not None: job['u02_holdout_policy']=policy
                append_job(jobs,result,job)
    finally:
        inputs.finish(); I.after()
        result['inputs']=[*I.meta.values(),*I.used.values()]
        if ledger.exists(): result['fresh_early_bindings']=U.pin(ledger)
        result['source_bytes_verified_before_after']=True


def legacy_sources(record, document, I, output):
    """The original pointer/value predicates with an explicit portable reader."""
    P=U.original('accept_legacy_prefix')
    catalog={}
    for p in document['inputs']:
        q={k:p[k] for k in ('path','bytes','sha256')}
        U.need(q['path'] not in catalog or catalog[q['path']]==q,'Conflicting legacy input catalog')
        catalog[q['path']]=q
    get=lambda ref:I.resolve(ref,catalog)
    P.source_negative_gate(record,record['coefficients_low_to_high'],record['vector_reference'],output)
    ref=record['vector_reference']; source=get(ref); actual=P.pointer(source,ref['json_pointer'])
    P.source_negative_gate(record,actual,ref,output)
    U.need(actual==record['coefficients_low_to_high'],'Original vector/source-map coefficients differ')
    U.need(U.sha(U.encoded(P.pointer(source,ref['record_pointer'])))==ref['record_sha256'],'Original full source record hash differs')
    tref=record['triple_reference']
    U.need(P.triple(P.pointer(get(tref),tref['json_pointer']))==P.triple(record['bare_triple']),'Original bare triple pointer differs')
    for extra in record.get('additional_vector_sources',[]):
        resolved=P.alternate_reference(record,extra); actual=P.pointer(get(resolved),resolved['json_pointer'])
        P.source_negative_gate(record,actual,resolved,output)
        U.need(list(map(P.rational,actual))==list(map(P.rational,record['coefficients_low_to_high'])),'Additional source vector differs')
    if record.get('adopted_disposition_reference'):
        ar=record['adopted_disposition_reference']; P.pointer(get(ar),ar['json_pointer'])


def legacy_index(recipe, op, output, deadline, result):
    I=U.Inputs(recipe); P=U.original('accept_legacy_prefix'); L=U.original('index_legacy_recounts'); T=U.original('index_legacy_tail_recounts')
    G,_=configure_geometry(recipe)
    document=U.read(I.meta['legacy_vectors']['path']); chosen=U.read(I.meta['chosen_terminals']['path'])
    all_records=P.metadata_roster(document,chosen,prefix_ids=tuple(range(297)))
    tables={}; mask_pins={}
    try:
        with output.with_suffix('.jobs.jsonl').open('xb') as stream:
            for expected in op['records']:
                deadline.check(); record=all_records[expected['id']]
                U.need(U.sha(U.encoded(record))==expected['compact_sha256'],'Original legacy metadata record changed')
                legacy_sources(record,document,I,output)
                if record['id']<272:
                    job=L.make_job(record,G,U.pin(G.__file__))
                    independently=P.original_model(record['bare_triple'])
                    U.need(set(job['model'])==set(independently)|{'geometry_premise'} and
                           all(job['model'][k]==v for k,v in independently.items()),'Two preserved original-hive constructions disagree')
                else:
                    original=T.original_hive(record['bare_triple']); n=original['rank']
                    U.need(n in (6,7),'Unsupported tail forcing rank')
                    if n not in tables:
                        name=f'namespaces/base/methods/frontier-025-2026-09-10/science/results/F025-MASK-R{n}-001.json'
                        tables[n]=I.document(name); mask_pins[n]=I.used[name]
                        U.need(mask_pins[n]['sha256']==T.MASK_SHA[n],'Accepted forcing table bytes changed')
                    accepted=T.canonical_mask(tables[n],n,original['boundary_mask'])
                    ref={**mask_pins[n],'json_pointer':f"/records/{original['boundary_mask']}",'record_sha256':U.sha(U.encoded(accepted))}
                    job=T.make_job(record,original,accepted,ref)
                job['portable_source_metadata']=I.meta['legacy_vectors']
                job['original_source_pointer_validation']='Original whole-file bytes, source row, vector, triple and alternate pointers checked; theorem acceptance remains separate'
                append_job(stream,result,job)
    finally:
        I.after(); result['inputs']=[*I.meta.values(),*I.used.values()]
        result['portable_source_resolutions']=I.resolutions
        result['source_bytes_verified_before_after']=True


def index(recipe, op, output, deadline, result):
    R=U.original('recount_records')
    ids=[r['id'] for r in op['records']]
    result.update(schema=R.SCHEMA,kind='manifest',status='PARTIAL',unit=op['unit'],stream=op['stream'],
                  input_root=recipe['data_root'],expected_record_ids=sorted(ids),records=[],pending_index_ids=sorted(ids),
                  selection_complete=True,index_complete=False,inputs=[],wrapper_sha256=U.pin(R.__file__)['sha256'],
                  indexer=U.pin(__file__),source_roster=op['roster'],source_slice=op['slice'],
                  explicit_source_records=op['records'],scope=U.SCOPE)
    try:
        if op['cohort']=='production': production_index(recipe,op,output,deadline,result)
        elif op['cohort'] in ('U02','U03'): early_index(recipe,op,output,deadline,result)
        else: legacy_index(recipe,op,output,deadline,result)
    finally:
        entries=result['records']; completed=[r['id'] for r in entries]
        U.need(completed==ids[:len(completed)],'Index does not describe an exact completed source prefix')
        result['pending_index_ids']=sorted(set(ids)-set(completed))
        result['index_complete']=completed==ids
        result['status']='FROZEN_RECOUNT_JOBS' if result['index_complete'] else 'PARTIAL'
        path=output.with_suffix('.jobs.jsonl')
        if path.exists(): result['jobs']=U.pin(path)
        result['inputs']=list({p['path']:p for p in [*result.get('inputs',[]),*result.get('portable_accessed_sources',[]),
                               *recipe['metadata'].values(),*recipe['code'],op['roster'],U.pin(__file__),U.pin(R.__file__)]}.values())
        for p in result['inputs']: U.check(p)
