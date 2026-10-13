"""Complete selected absorber replay on exactly the original fixed fixtures."""
import argparse,pathlib,sys
import verify_absorber
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
r=pathlib.Path(__file__).resolve().parents[1]
args=['--mode','verify','--source-index',str(r/'SOURCE-MAP.json'),'--proof',str(r/'proofs/pro048/U01-01-TWO-CAP-RANK-SEVEN-POSITIVITY.md'),'--tables',str(r/'proofs/pro048/U01-01-CERTIFICATE-TABLES.md'),'--factor',str(r/'data/absorber/FACTOR-CLASS.json'),'--boundary-class',str(r/'data/absorber/BOUNDARY-CLASS.json'),'--positive-payment',str(r/'data/absorber/MULTIGAP-MERGE-RESERVE.json'),'--boundary-payment',str(r/'data/absorber/BOUNDARY-MERGE-RESERVE.json')]
for pair in ('11','12','22'):args+=['--bare'+pair,str(r/('data/absorber/A-pair-'+pair+'-bare.json'))]
args+=['--original-counter',str(r/'code/original_lr.py'),'--out',a.out]
sys.argv=[sys.argv[0]]+args;verify_absorber.main()
