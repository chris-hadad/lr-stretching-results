"""New Python-integer scan of every declared q7 field row (data only).
Independent authored control flow; schemas read from U02 FORMATS.md and the
jet serialization header. Provider checker implementations are not imported.
"""
from pathlib import Path
from fractions import Fraction
from array import array
import hashlib,json,math,mmap,struct,sys,time,traceback
if sys.flags.optimize:
    raise SystemExit('REFUSED: Python assertions must be enabled for check_field.py')
DATA=Path(sys.argv[1]);END=int(sys.argv[2]);RUN=Path(sys.argv[3]);TAG=sys.argv[4]
if (RUN/f'{TAG}.json').exists() or (RUN/f'{TAG}-ADVERSE.jsonl').exists():
    raise SystemExit('REFUSED: fresh field output required')
start=time.monotonic();adverse=RUN/f'{TAG}-ADVERSE.jsonl'
def fail_record(x):
    with adverse.open('a') as f:f.write(json.dumps(x)+'\n');f.flush()
def mapped(p):
    f=p.open('rb'); m=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ);f.close();return m
try:
    declaration=json.loads((DATA/'U04/INPUTS.json').read_text()); bindings=[]
    for spec in declaration['files']:
        p=DATA/spec['path'];h=hashlib.sha256()
        with p.open('rb') as f:
            while chunk:=f.read(2**20):h.update(chunk)
        observed={'path':spec['path'],'bytes':p.stat().st_size,'sha256':h.hexdigest()};bindings.append(observed)
        assert (observed['bytes'],observed['sha256'])==(spec['bytes'],spec['sha256']),observed
    raw=(DATA/'U04/DATA/FIELD.i64').read_bytes();field=array('q');field.frombytes(raw)
    if sys.byteorder!='little':field.byteswap()
    assert hashlib.sha256(raw).hexdigest()==declaration['field_sha256']
    assert len(field)==2702884
    field_summary={'entries':len(field),'nonzero':sum(x!=0 for x in field),'max_abs':max(map(abs,field)),'all_multiples_of_six':all(x%6==0 for x in field)}
    assert field_summary=={'entries':2702884,'nonzero':1347074,'max_abs':119981311320,'all_multiples_of_six':True}
    scalars=[];scalar_min=None;negtypes=0;bits=0
    with (DATA/'U03-A05/DATA/CACHE/q7.jets').open() as f:
        assert f.readline().split()==['P31JETS1','7','0','1651060','1']
        for i,line in enumerate(f):
            tokens=line.split();assert len(tokens)==3,(i,tokens)
            ident,b,a=map(int,tokens);assert ident==i and b>0 and math.gcd(a,b)==1,(i,tokens)
            scalars.append((a,b));negtypes+=a<0;bits=max(bits,abs(a).bit_length(),b.bit_length())
            if scalar_min is None or a*scalar_min[1]<scalar_min[0]*b:scalar_min=(a,b,i)
    assert len(scalars)==1651060
    joins=mapped(DATA/'U02/DATA/q7.join');lookup=mapped(DATA/'U02/DATA/q7.lookup')
    rhs=mapped(DATA/'U03-A05/DATA/RHS-ORBIT-TYPES.u32');types=mapped(DATA/'U02/DATA/q7.types');maps=mapped(DATA/'U02/DATA/q7-ALL.map')
    assert len(joins)==12*2999563 and len(lookup)==8*math.comb(42,7)
    assert len(rhs)==4*2999563 and len(types)==73*len(scalars) and len(maps)==6*math.comb(42,7)
    loading=time.monotonic()-start;scan_start=time.monotonic();sixD=6*10**12
    uses=array('I',[0])*len(scalars);originals=neg_originals=0
    row=nnz=maxl1=maxdot=negative=zero=below=rawnegative=0;previous_ordinal=-1;minimum=None;witness=None
    for shard in declaration['shards']:
        assert shard['begin']==row,(shard,row)
        if row>=END:break
        payload=(DATA/shard['path']).read_bytes();pos=0
        while pos<len(payload):
            ordinal,count=struct.unpack_from('<IH',payload,pos);pos+=6
            assert previous_ordinal<ordinal and 0<count<=28,(row,ordinal,count)
            previous_ordinal=ordinal
            joined,type_id,code=struct.unpack_from('<III',joins,12*row)
            lookup_type,lookup_code=struct.unpack_from('<II',lookup,8*ordinal)
            rhs_type=struct.unpack_from('<I',rhs,4*row)[0]
            assert ordinal==joined and type_id==lookup_type==rhs_type and code==lookup_code,(row,ordinal)
            permutation=tuple((code>>(3*i))&7 for i in range(7))
            assert sorted(permutation)==list(range(7)) and code>>(3*7)==0
            representative,index,mask=struct.unpack_from('<IBB',maps,6*ordinal)
            assert representative==ordinal and index==types[73*type_id] and mask and mask<64 and 6%mask.bit_count()==0
            orbit=6//mask.bit_count();originals+=orbit
            a,b=scalars[type_id];rawnegative+=a<0;neg_originals+=orbit*(a<0);uses[type_id]+=1
            dot=l1=0;lastcol=-1;entries=[]
            for col,value in struct.iter_unpack('<Ii',payload[pos:pos+8*count]):
                assert lastcol<col<len(field) and value and abs(value)<=20,(row,col,value)
                lastcol=col;dot+=value*field[col];l1+=abs(value)
                if ordinal==1303913:entries.append((col,value))
            pos+=8*count;nnz+=count;maxl1=max(maxl1,l1);maxdot=max(maxdot,abs(dot))
            numerator=sixD*a+b*dot
            negative+=numerator<0;zero+=numerator==0;below+=200000000*numerator<sixD*b
            if numerator<=0 or 200000000*numerator<sixD*b:
                fail_record({'kind':'LOCAL_FIELD_BOUND_FAILURE','row':row,'ordinal':ordinal,'type_id':type_id,'raw_alpha':str(Fraction(a,b)),'Bv':dot,'beta':str(Fraction(numerator,sixD*b)),'whole_LR_negative':False})
            if minimum is None or numerator*minimum['denominator']<minimum['numerator']*b:
                minimum={'numerator':numerator,'denominator':b,'row':row,'ordinal':ordinal,'type_id':type_id,'Bv':dot}
            if ordinal==1303913:witness={'row':row,'ordinal':ordinal,'type_id':type_id,'raw_alpha':str(Fraction(a,b)),'Bv':dot,'entries':entries,'beta':str(Fraction(numerator,sixD*b))}
            row+=1
        assert pos==len(payload) and row==shard['end'],(pos,len(payload),row,shard)
    scan_seconds=time.monotonic()-scan_start
    assert row==END,(row,END)
    result={'status':'PASS_EXACT_DECLARED_FIELD_ROWS' if negative==zero==below==0 else 'FAIL_FIELD','end':END,'rows':row,'nonzeros':nnz,'field':field_summary,'scalar_types':len(scalars),'negative_scalar_types':negtypes,'scalar_max_integer_bits':bits,'minimum_raw_type':scalar_min[2],'minimum_raw_alpha':str(Fraction(scalar_min[0],scalar_min[1])),'raw_negative_rows':rawnegative,'original_subsets_by_supplied_stabilizers':originals,'negative_originals_by_supplied_stabilizers':neg_originals,'negative_corrected_rows':negative,'zero_corrected_rows':zero,'below_epsilon':below,'maximum_abs_Bv':maxdot,'maximum_l1':maxl1,'minimum':{k:v for k,v in minimum.items() if k not in ('numerator','denominator')},'minimum_beta':str(Fraction(minimum['numerator'],sixD*minimum['denominator'])),'loading_seconds':loading,'scan_seconds':scan_seconds,'total_seconds':time.monotonic()-start,'all_row_estimate_seconds':loading+scan_seconds*2999563/row,'bindings':bindings,'returned_code_executed':False,'scope':'Exact field inequalities and declared full scalar/operator/join consistency. Does not derive scalar values from BV or regenerate complete topology.'}
    if END==2999563:
        assert nnz==38215504 and min(uses)>0 and sum(uses)==row
        for ident,u in enumerate(uses):assert u==struct.unpack_from('<I',types,73*ident+65)[0],ident
        result['all_types_used']=True;result['maximum_type_reuse']=max(uses)
    if witness:
        claim=json.loads((DATA/'U04/DATA/MINIMUM-WITNESS.json').read_text())
        assert witness['entries']==[tuple(x) for x in claim['row_entries']]
        delta=claim['changed_delta'];coordinate=claim['changed_coordinate']
        wrongdot=witness['Bv']+dict(witness['entries'])[coordinate]*delta
        wrong=Fraction(witness['raw_alpha'])+Fraction(wrongdot,sixD)
        control={'kind':'INTENTIONAL_CHANGED_FIELD_CONTROL','coordinate':coordinate,'delta':delta,'wrong_Bv':wrongdot,'wrong_beta':str(wrong),'whole_LR_negative':False}
        fail_record(control)
        assert wrong<0 and str(wrong)==claim['wrong_beta'];result['adverse_control']=control;result['witness']=witness
    (RUN/f'{TAG}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('bindings','witness')}))
    assert result['status']=='PASS_EXACT_DECLARED_FIELD_ROWS'
except Exception as exc:
    fail_record({'kind':'ERROR','exception':repr(exc),'traceback':traceback.format_exc(),'whole_LR_negative':False});raise
