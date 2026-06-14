import subprocess
import sys
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent / "src"


def run(module_name: str) -> None:
    print(f"==== Starte {module_name} ====", flush=True)
    subprocess.run(
        [sys.executable, "-m", module_name],
        cwd=SRC_DIR,
        check=True,
    )
    print()


run("oo_test.main")
run("repo_test.main")
