"""Run the bounded exact controls. The proof supplies the universal statements."""
from pathlib import Path
import subprocess, sys
if sys.flags.optimize:
    raise RuntimeError('Run with assertions enabled; omit -O and PYTHONOPTIMIZE')
root=Path(__file__).resolve().parent
for args in [('interface_checker.py','--verify-fields','0','--verify-fields','1'),
             ('sector_fields.py',),('projection_controls.py',)]:
    subprocess.run([sys.executable,'-B',str(root/args[0]),*args[1:]],check=True)
