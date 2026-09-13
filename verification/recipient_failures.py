"""Fresh external recipient-failure fixtures for the unchanged finite-box facade."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
import argparse
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--module',type=Path,required=True)
p.add_argument('--data',type=Path,required=True)
p.add_argument('--work',type=Path,required=True)
a=p.parse_args()
MODULE=a.module.resolve();DATA=a.data.resolve();BASE=a.work.resolve()
assert MODULE.is_dir() and DATA.is_dir()
assert not BASE.is_relative_to(MODULE) and not BASE.is_relative_to(DATA)
BASE.mkdir(exist_ok=False)
observed=[]
def run(name,args,expected=2):
 result=subprocess.run([sys.executable,'-I','-S','-B',str(MODULE/'verify.py'),*args],capture_output=True,text=True,timeout=110)
 (BASE/(name+'.stdout.txt')).write_text(result.stdout)
 (BASE/(name+'.stderr.txt')).write_text(result.stderr)
 assert result.returncode==expected,(name,result.returncode,result.stdout,result.stderr)
 if expected:
  messages=[json.loads(line) for line in (result.stdout+'\n'+result.stderr).splitlines() if line.startswith('{')]
  assert any(m.get('status') in ('REFUSED','RECIPIENT_COMMAND_REFUSED') for m in messages)
  assert not any(m.get('status')=='PASS' for m in messages)
 observed.append({'name':name,'exit_code':result.returncode,'stderr':result.stderr.strip()})

missing=BASE/'empty-data';missing.mkdir()
run('missing-data',['inventory','--data',str(missing),'--work',str(BASE/'missing-work')])
assets=BASE/'empty-assets';assets.mkdir()
# The extraction script's own typed refusal is returned by the facade unchanged.
x=subprocess.run([sys.executable,'-I','-S','-B',str(MODULE/'verify.py'),'extract','--assets',str(assets),'--data',str(BASE/'bad-extract')],capture_output=True,text=True,timeout=110)
assert x.returncode!=0 and not (BASE/'bad-extract.EXTRACTION.json').exists()
observed.append({'name':'missing-archive','exit_code':x.returncode,'stderr':x.stderr.strip(),'stdout':x.stdout.strip()})

spec=importlib.util.spec_from_file_location('box_facade',MODULE/'verify.py');facade=importlib.util.module_from_spec(spec);spec.loader.exec_module(facade)
contract=facade.module_contract(MODULE)
interrupted=BASE/'interrupted-after-prepare'
parameters=facade.parameters(contract,'inventory',DATA,interrupted)
result=subprocess.run(facade.prepare_command(parameters),capture_output=True,text=True,timeout=110)
assert result.returncode==0 and (interrupted/'PLAN.json').is_file() and not (interrupted/'FACADE-PARAMETERS.json').exists()
before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in interrupted.iterdir() if p.is_file()}
run('interrupted-prepare-refused',['inventory','--data',str(DATA),'--work',str(interrupted)])
after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in interrupted.iterdir() if p.is_file()}
assert before==after,'Refusal changed preserved incomplete evidence'

good=BASE/'changed-parameters'
run('fresh-inventory-control',['inventory','--data',str(DATA),'--work',str(good)],expected=0)
run('changed-batch-refused',['inventory','--data',str(DATA),'--work',str(good),'--jobs-per-call','17'])
orphan=good/'calls/call-000001';orphan.mkdir()
run('unrecorded-call-refused',['inventory','--data',str(DATA),'--work',str(good)])
assert orphan.is_dir(),'Refusal removed the adverse observation'
print(json.dumps({'status':'PASS','scope':'Missing data/archive, interrupted preparation, changed frozen parameters and unrecorded call directory; no full mathematical replay.','observations':observed},indent=2))
