"""Fixed lifecycle probe used only by the interruption controls."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

if len(sys.argv)!=2:raise SystemExit(2)
child=subprocess.Popen([sys.executable,"-c","import time; time.sleep(300)",sys.argv[1]])
with Path(sys.argv[1]).open("x") as stream:
    json.dump({"pid":os.getpid(),"pgid":os.getpgrp(),"grandchild_pid":child.pid},stream)
    stream.write("\n")
time.sleep(300)
