"""Full 40-chamber A64 finite certificate replay."""
import argparse,pathlib,sys
import verify_two_cap
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parents[1]
args=[]
for k in range(4,9):args+=['--cert',str(r/('data/crossing/TWO-CAP-a'+str(k)+'.json'))]
sys.argv=[sys.argv[0]]+args+['--out',a.out];raise SystemExit(verify_two_cap.main())
