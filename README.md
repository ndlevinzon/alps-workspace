# ALPS workspace

Umbrella checkout for four independent GitHub repos. ALPS orchestrates
ligandparam, scission, and ffpopt; each subdirectory is its own git repo.

| Folder (after clone) | Package | Remote |
|----------------------|---------|--------|
| `alps-main` | `alps` | https://github.com/ndlevinzon/alps |
| `ligandparam-main` | `ligandparam` | https://github.com/ndlevinzon/ligandparam |
| `scission-main` | `scission` | https://github.com/ndlevinzon/scission |
| `ffpopt-main` | `ffpopt` | https://github.com/ndlevinzon/ffpopt |

Open `alps.code-workspace` in Cursor/VS Code so each repo is a named git root.

## Documentation

Combined Sphinx API reference for all four packages lives in this repo
(`docs/`), not in the individual tool checkouts.

```bash
pip install -r docs/requirements.txt
cd docs
python gen_api.py
sphinx-build -b html . _build/html
```

Open `docs/_build/html/index.html`. Re-run `python gen_api.py` after adding
or renaming modules. Developer guide, design notes, and tutorials are
stubbed under `docs/guide/` for later.

## Two-push workflow

1. Commit and push inside the tool you edited.
2. In this workspace root, commit the updated submodule pointer and push.

A change that spans two tools is three pushes (both tools, then this workspace).

---

## Install (HPC / conda)

This is the supported way to stand up the full stack: **Python 3.12**,
**conda-forge AmberTools**, **ParmEd 4.3+**, and **numpy whatever AmberTools
needs**. Do not pin `parmed==4.0.0` (no py312 build) and do not use
`alps-main/env.yaml` for this (that file is an orchestrator-only leftover).

ffpopt's CMake build requires Python 3.12. Create the env on a **compute
node**, not a login node.

### 1. Clone

```bash
git clone --recurse-submodules https://github.com/ndlevinzon/alps-workspace.git
cd alps-workspace
git submodule update --init --recursive
```

### 2. Conda environment

```bash
module load miniconda3    # site-specific; skip if conda/mamba is already on PATH
mamba env create -f env.yaml   # or: conda env create -f env.yaml
conda activate alps
source "${CONDA_PREFIX}/amber.sh"   # sets AMBERHOME from conda AmberTools
```

Check the pins that actually matter:

```bash
which antechamber parmchk2 tleap
python -c "import sys, numpy, parmed; print(sys.version.split()[0], numpy.__version__, parmed.__version__)"
```

Expect Python `3.12.x` and ParmEd `4.3.x` or newer. Current conda-forge
AmberTools py312 builds often pull **numpy 2.x**; that is OK for this env.
Leave conda's numpy alone (see pip `--no-deps` below).

### 3. Python packages (ALPS last)

Editable installs use `--no-deps` so pip does not downgrade conda AmberTools /
numpy / ParmEd. `ndfes` and `nispo` are pip-only (ffpopt).

```bash
python -m pip install -U pip
python -m pip install ndfes nispo

python -m pip install -e ligandparam-main --no-deps
python -m pip install -e scission-main --no-deps

ACADEMIC=TRUE python -m pip install -e ffpopt-main --no-deps

python -m pip install -e "./alps-main[dihed,tblite]" --no-deps
```

Install ALPS last so it owns `lig-getparam`. ligandparam also declares that
console script; whichever pip ran last wins.

`ACADEMIC=TRUE` is only for ffpopt's CMake model fetch. Skip it in industry
deployments and use `--model xtb` (tblite is already in the env).

### 4. Gaussian (optional)

Needed for `lazyligand` / `freeligand` RESP recipes, not for `--model xtb`
twist or `lazierligand`.

```bash
module load gaussian/g16    # site-specific
which g16
```

### 5. Verify

```bash
which lig-getparam lig-dihed-correct lig-scission scission
python -c "
import alps, ligandparam, scission, ffpopt
from alps.companions import print_status_line
print('alps', alps.__version__)
print_status_line()
"

( cd alps-main && python -m unittest tests.test_install_validation -v )
( cd ligandparam-main && python -m unittest discover -s tests -v )
( cd scission-main && python -m unittest discover -s tests -v )
```

Companions should resolve as `sibling` or `installed`.

### Typical job

```bash
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 44
#SBATCH -t 24:00:00
#SBATCH -A <account>

module purge
module load miniconda3
# module load gaussian/g16   # only for Gaussian RESP recipes

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate alps
source "${CONDA_PREFIX}/amber.sh"

export OMP_NUM_THREADS=1

cd /path/to/work
lig-getparam -i chaps.mol2 -r CHA -d CHA3 -rn lazierligand --net_charge 0 -n 10 --mem 32
lig-dihed-correct -d CHA3 -r CHA --label chaps --model xtb -n 44
```

`lazierligand` is BCC / Antechamber (no Gaussian). Switch `-rn lazyligand` or
`freeligand` when `g16` is loaded. Keep this env on **xtb**; qdpi2 / aimnet2
are separate ML stacks (TensorFlow vs PyTorch) and do not mix.

### Solver / runtime notes

- `parmed==4.0.0` + `python=3.12` does not solve. Use ParmEd 4.3+.
- Do not create the env from `ffpopt-main/environment.yml` (psi4 / pytorch /
  tensorflow kitchen sink).
- If `pip install -e ffpopt-main` fails on CMake, ALPS can still bind
  `ffpopt-main/src/python/lib` as a sibling checkout; `geometric` and `tblite`
  must already be in the env.
- If `lig-getparam` prints no ALPS banner, ligandparam was installed after
  ALPS — reinstall `./alps-main`.
- Load `amber.sh` in every job, not only in the install shell.
