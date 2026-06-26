import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"


def main() -> None:
    print("==== Phase-3-Application ====", flush=True)
    umgebung = dict(os.environ)
    umgebung["PYTHONPATH"] = str(SRC)
    ergebnis = subprocess.run(
        [sys.executable, "-m", "bootstrap.main"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        env=umgebung,
    )
    if ergebnis.stdout:
        print(ergebnis.stdout, end="")
    if ergebnis.stderr:
        print(ergebnis.stderr, end="")
    print()


if __name__ == "__main__":
    main()
