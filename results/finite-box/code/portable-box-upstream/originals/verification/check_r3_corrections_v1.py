"""Exact small-certificate population join and two review boundary controls."""
import argparse,hashlib,json,os,time
from pathlib import Path
from fractions import Fraction as Q

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def key(parts):
    padded=[tuple(p)+(0,)*(7-len(p)) for p in parts]
    assert all(len(p)==7 for p in padded)
    return (padded[0],*sorted(padded[1:]))
def H(b):
    l,m,n=[tuple(p)+(0,)*(6-len(p)) for p in b]
    return -l[0]-l[3]-l[4]+m[0]+m[3]+m[4]+n[0]+n[1]+n[2]

def main():
    p=argparse.ArgumentParser();p.add_argument('--roster',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=json.loads(a.roster.read_text());start=time.monotonic()
    cert=json.loads(Path(r['certificate']).read_text());cover=json.loads(Path(r['cover']).read_text())
    assert cert['status']==cover['status']=='complete'
    records=cert['records'];by_key={key([x['boundary'][s] for s in ['lambda','mu','nu']]):x['id'] for x in records}
    assert len(records)==len(by_key)==56
    original=set();summary={};joins=[]
    for name in ['original6','original7','global']:
        found=set();count=0;pre=[0,0];last=0
        with Path(r[name]).open() as f:
            header=next(f).rstrip('\n')
            assert header==('id\trank\tlambda\tmu\tnu\toriginal_rank6_preimages\toriginal_rank7_preimages' if name=='global' else 'lambda\tmu\tnu\tchart_bound')
            for line in f:
                z=line.rstrip('\n').split('\t');parts=z[2:5] if name=='global' else z[:3]
                if name=='global':
                    id=int(z[0]);assert id==last+1;last=id
                l=tuple(map(int,parts[0].split(',')))
                if sum(l)>16:continue
                parts=[l,*[tuple(map(int,x.split(','))) for x in parts[1:]]];identity=key(parts)
                assert identity in by_key and identity not in found
                found.add(identity);count+=1
                if name=='global':
                    pre=[pre[i]+int(z[5+i]) for i in range(2)]
                    joins.append({'global_id':id,'certificate_id':by_key[identity],'rank':int(z[1]),'boundary':dict(zip(['lambda','mu','nu'],parts)),'preimages':list(map(int,z[5:7]))})
        if name=='global':assert last==4747974 and found==set(by_key)==original and pre==[526,556]
        else:original|=found
        summary[name]={'rows':count,'unique_identities':len(found),'missing_certificate':0,'preimages':pre if name=='global' else None}
    assert summary['original6']['rows']==37 and summary['original7']['rows']==19 and len(original)==56
    assert cover['branches']['small']=={'keys':56,'rank6_keys':37,'rank7_keys':19,'original_rank6':526,'original_rank7':556}
    b=((2,)*6,(2,)*3,(1,)*6)
    ray_a=((3,2,2,2,1,0),(2,2,2,1,0,0),(2,1,0,0,0,0))
    ray_c=((4,3,2,2,2,1),(2,2,1,0,0,0),(2,2,2,2,1,0))
    assert sum(b[0])==sum(b[1])+sum(b[2]) and H(b)==-1 and H(ray_a)==H(ray_c)==0
    assert all(all(y<=x for x,y in zip(b[0],q)) for q in b[1:])
    q=4;eta=Q(1,2);kappa=Q(8);linear=(q*q*eta-kappa)/q
    assert kappa==q*q*eta and linear==0
    result={'status':'complete','pid':os.getpid(),'pgid':os.getpgrp(),'native_calls':0,
            'input_sha256':{name:sha(path) for name,path in r.items()},'small_join':summary,'records':joins,
            'small_original_preimages':1082,'global_cover_result_sha256':sha(r['cover']),
            'feasibility_control':{'boundary':b,'H':-1,'H_a':0,'H_c':0,'scope':'Linearity leaves H=-1 on the complete translated family, so its fibers stay empty.'},
            'residual_control':{'Reeve_parameter':10,'q':q,'eta':str(eta),'kappa':str(kappa),'residual_coefficients':['1','0','1/2'],'scope':'Weak inequality gives coefficientwise nonnegative residual; strict inequality is required for its positive linear coefficient.'},
            'seconds':time.monotonic()-start,'scope':'Exact source/identity join and algebraic boundary controls; no new LR scalar counts or additive population credit.'}
    with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':'complete','joined_keys':len(joins),'preimages':1082,'seconds':result['seconds']}))
if __name__=='__main__':main()
