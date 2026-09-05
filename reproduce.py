"""Reproduce all five mathematical modules using Python's standard library."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROGRAMS = (
    "results/hurwitz-counterexample/reproduce.py",
    "results/hurwitz-cone/reproduce.py",
    "results/parabolic-a3/a3_reproduce.py",
    "results/coefficient-cone/reproduce.py",
    "results/two-row-nonconcavity/two_row.py",
)


def main():
    for program in PROGRAMS:
        print(program, flush=True)
        subprocess.run([sys.executable, "-B", str(ROOT/program)],
                       cwd=ROOT, check=True, timeout=120)
    print("All five mathematical modules reproduced.")


if __name__ == "__main__":
    main()
