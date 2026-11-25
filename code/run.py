"""The Makefile's targets for any OS (Windows has no make). Run from this folder:

    python run.py reports            # or: install, install-r, test, data, benchmark1, benchmark2, figures, check-aux
    python run.py test reports       # several targets, in order

Each target runs the same commands as the Makefile, with this interpreter and with PYTHONPATH set to src/ and this
folder, so nothing needs exporting first. check-aux checks data/ against benchmarks/liana_final/aux_files.md5 (what
`md5sum -c` does on Linux).
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M = [sys.executable, "-m"]
TARGETS = {
    "install": [M + ["pip", "install", "-r", "requirements.txt"], M + ["pip", "install", "--no-deps", "-e", "."]],
    "install-r": [["Rscript", "tools/cellchat/install_r_packages.R"]],
    "test": [M + ["pytest", "-q"]],
    "data": [M + ["ccc_nulls.datasets", "tnbc_wu2021", "allen_brain_atlas", "tabula_sapiens_mammary",
                  "tabula_sapiens_liver", "tabula_sapiens_lung"]],
    "benchmark1": [M + ["benchmarks.liana_nulls", "--part", "core"],
                   M + ["benchmarks.liana_nulls", "--part", "core", "--dataset", "moffitt2018_hypothalamus"],
                   M + ["benchmarks.liana_nulls", "--part", "calibration", "power", "biology", "amendment", "extend",
                        "power_a3", "b2_validity", "ablation", "report"],
                   M + ["benchmarks.liana_nulls.amendment4", "--part", "all"],
                   M + ["benchmarks.liana_nulls.amendment5", "--part", "all"]],
    "benchmark2": [M + ["benchmarks.liana_final", "--part", "all"]] +
                  [M + [f"benchmarks.liana_final.amendment{i}", "--part", "all"] for i in range(2, 10)],
    "reports": [M + ["benchmarks.liana_nulls", "--part", "report"], M + ["benchmarks.liana_final", "--part", "report"]] +
               [M + [f"benchmarks.liana_final.amendment{i}", "--part", "report"] for i in (2, 3, 4, 6)] +
               [M + ["benchmarks.liana_final.report_amendment7"]] +
               [M + [f"benchmarks.liana_final.amendment{i}", "--part", "report"] for i in (8, 9)],
    "figures": [[sys.executable, "figures/make_figures.py"]],
}
NEEDS = {"benchmark1": ["data"], "benchmark2": ["data"]}


def check_aux() -> int:
    bad = 0
    for line in (HERE / "benchmarks/liana_final/aux_files.md5").read_text().splitlines():
        if not line.strip():
            continue
        md5, name = line.split(maxsplit=1)
        f = HERE / "data" / name.strip().lstrip("*")
        ok = f.is_file() and hashlib.md5(f.read_bytes()).hexdigest() == md5
        bad += not ok
        print(f"{name}: {'OK' if ok else 'FAILED' if f.is_file() else 'MISSING'}")
    return 1 if bad else 0


def run(target: str, done: set) -> int:
    if target in done:
        return 0
    for dep in NEEDS.get(target, []):
        if run(dep, done):
            return 1
    done.add(target)
    if target == "check-aux":
        return check_aux()
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(HERE / "src"), str(HERE)]))
    for cmd in TARGETS[target]:
        print("+", " ".join(cmd), flush=True)
        if subprocess.call(cmd, cwd=HERE, env=env):
            return 1
    return 0


if __name__ == "__main__":
    names = sys.argv[1:]
    unknown = [t for t in names if t not in TARGETS and t != "check-aux"]
    if not names or unknown:
        sys.exit(__doc__ + (f"\nunknown target(s): {', '.join(unknown)}" if unknown else ""))
    done: set = set()
    sys.exit(next((1 for t in names if run(t, done)), 0))
