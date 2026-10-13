"""Complete accepted A61 rational chamber/balancing certificate."""
from fractions import Fraction as F
from pathlib import Path
import argparse, json, time, hashlib

def inv(A):
    n=len(A);rows=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        q=next(i for i in range(j,n) if rows[i][j]);rows[j],rows[q]=rows[q],rows[j]
        v=rows[j][j];rows[j]=[x/v for x in rows[j]]
        for i in range(n):
            if i!=j:
                v=rows[i][j];rows[i]=[x-v*y for x,y in zip(rows[i],rows[j])]
    return [r[n:] for r in rows]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();start=time.monotonic()
    src=Path(__file__).with_name('chambers-v1.json');data=json.loads(src.read_text());rows=[]
    for row in data['chambers']:
        Ainv=inv(row['parameter_rows']);p={tuple(x['powers']):F(x['coefficient']) for x in row['coefficients']}
        for small,big in [(0,1),(0,2),(1,2)]:
            direction=[v[small]-v[big] for v in Ainv];d={}
            for powers,c in p.items():
                for j,v in enumerate(direction):
                    if powers[j] and v:
                        k=list(powers);k[j]-=1;k=tuple(k);d[k]=d.get(k,F(0))+c*powers[j]*v
            d={k:v for k,v in d.items() if v}
            neg=[{'powers':list(k),'coefficient':str(v)} for k,v in sorted(d.items()) if v<0]
            rows.append(dict(chamber=row['chamber'],small=small,big=big,direction=list(map(str,direction)),coefficients=[dict(powers=k,coefficient=str(v)) for k,v in sorted(d.items())],negative=neg))
    report=dict(schema='a61-balancing-derivatives/v1',status='PASS' if not any(x['negative'] for x in rows) else 'SIGNED-COORDINATE-OBSTRUCTION',seconds=time.monotonic()-start,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rows=rows,scope='A negative coefficient in chamber coordinates is a certificate obstruction, not a negative evaluated gain or an LR candidate.')
    with args.out.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps({'status':report['status'],'negative_rows':[{k:x[k] for k in ['chamber','small','big']} | {'negative_count':len(x['negative']),'first':x['negative'][:1]} for x in rows if x['negative']],'seconds':report['seconds']}))
if __name__=='__main__':main()
