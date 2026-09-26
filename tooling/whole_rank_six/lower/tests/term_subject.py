"""Small cancellation subject for the staged adapter tests; no science inputs."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import replay


def main():
    work = Path(sys.argv[1])
    replay.available_memory = lambda: 8 * 2**30
    replay.install_signal_handlers()
    child = [sys.executable, '-B', '-c',
             'import os,pathlib,signal,time,sys; '
             'blocked=signal.pthread_sigmask(signal.SIG_BLOCK,set()); '
             'pathlib.Path(sys.argv[2]).write_text(",".join(str(int(s)) for s in blocked)); '
             'pathlib.Path(sys.argv[1]).write_text(str(os.getpid())); '
             'time.sleep(60)',
             str(work/'child-pgid'), str(work/'child-mask')]
    try:
        replay.run_one(child, work/'child.process.json', None, 90)
    except InterruptedError:
        return 23
    return 24


if __name__ == '__main__':
    raise SystemExit(main())
