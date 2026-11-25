# CS690A Project 6: structure-preserving null models and FDR control for cell–cell communication

Permutation-based cell–cell communication tools (CellPhoneDB, CellChat, and LIANA+'s consensus built on them)
test each ligand–receptor interaction by permuting every cell's label at once, so an interaction is called as
soon as either the ligand or the receptor is specific to its cell type. We test instead whether both sides are
specific, with a bilateral permutation test (BPT, computed from the tools' own permutations), and compare it with a
matched-decoy test, a leave-one-out t-test and the tools' own test in two pre-registered benchmarks: each tool's
p-values, and LIANA+'s consensus ranking, on Tabula Sapiens, TNBC, Allen brain and mouse hypothalamus data with
known-null shuffles, planted interactions and spatial and downstream truths.

## Layout

```
ccc-null-models/
├── README.md     this file
├── report/       report.pdf, the final report
└── code/         the final code, with its own README.md: installation (Python and R), data sources and download,
                  the command for each result, folder structure
```

To reproduce: follow [`code/README.md`](code/README.md); its section 5 names the code behind every table and figure. In short, starting from this folder:

Linux / macOS (bash or zsh):

```bash
cd code
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install --no-deps -e .
export PYTHONPATH=$PWD/src:$PWD
python run.py test reports figures   # tests (no data), every results table and the report's three figures (seconds)
python run.py data                   # the data sets (about 9 GB), then: python run.py benchmark1 benchmark2
```

Windows (PowerShell):

```powershell
cd code
py -3.12 -m venv .venv; .venv\Scripts\Activate.ps1
pip install -r requirements.txt; pip install --no-deps -e .
$env:PYTHONPATH = "$PWD\src;$PWD"
python run.py test reports figures
python run.py data                   # then: python run.py benchmark1 benchmark2
```

`run.py` has the Makefile's targets for any OS; on Linux and macOS `make test`, `make reports` and so on do the same.
If PowerShell refuses to run `Activate.ps1`, allow local scripts once with
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

**Before `run.py data`:** two data sets (TNBC and Allen brain) came from Open Problems, whose download bucket is now
closed. Download them from the public Kaggle data set
[`kshitijbhardwaj1729/ccc-nulls-openproblems`](https://www.kaggle.com/datasets/kshitijbhardwaj1729/ccc-nulls-openproblems)
(Kaggle needs a free account) and put them in `code/data/` under the names in
[`code/data/README.md`](code/data/README.md); `run.py data` then checks their md5 and downloads the rest. The published runs used Linux (Kaggle, a lab server) and macOS.
