import subprocess
import sys
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent / "src"
CSV_DATEI = SRC_DIR / "data" / "module_database.csv"


def run(script_name: str) -> None:
    print(f"==== Starte {script_name} ====", flush=True)
    subprocess.run(
        [sys.executable, script_name],
        cwd=SRC_DIR,
        check=True,
    )
    print()


if CSV_DATEI.exists():
    CSV_DATEI.unlink()

run("csv_repository_test.py")
run("prognose_test.py")
