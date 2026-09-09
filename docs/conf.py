"""Sphinx configuration for the combined ALPS / companion API reference."""

from __future__ import annotations

import importlib
import importlib.util
import os
import sys
from pathlib import Path

_DOCS = Path(__file__).resolve().parent
_WORKSPACE = _DOCS.parent

# ---------------------------------------------------------------------------
# Optional science / ML stacks: mock before importing the four packages so
# Read the Docs (no AmberTools, no CMake ffpopt) can still autodoc.
# ---------------------------------------------------------------------------

_OPTIONAL_IMPORTS = [
    "rdkit",
    "parmed",
    "geometric",
    "jax",
    "jaxlib",
    "tblite",
    "xtb",
    "deepmd",
    "deepmd.infer",
    "torch",
    "torchvision",
    "torchani",
    "mace",
    "mace.calculators",
    "aimnet",
    "openbabel",
    "openff",
    "openff.toolkit",
    "ndfes",
    "nispo",
    "MDAnalysis",
    "psi4",
    "sander",
    "pysander",
    "fennol",
    "fennol.ase",
    "cuequivariance",
    "fairchem",
    "orb_models",
    "dgl",
    "espaloma_charge",
    "tensorflow",
    "netCDF4",
    "pytraj",
    "cpptraj",
    "openmm",
]


def _mock_if_missing(names: list[str]) -> list[str]:
    missing: list[str] = []
    for name in names:
        try:
            importlib.import_module(name)
        except Exception:
            missing.append(name)
    return missing


autodoc_mock_imports = list(_OPTIONAL_IMPORTS) if os.environ.get("READTHEDOCS") == "True" else _mock_if_missing(_OPTIONAL_IMPORTS)
if autodoc_mock_imports:
    from sphinx.ext.autodoc.mock import MockFinder

    for name in autodoc_mock_imports:
        for key in list(sys.modules):
            if key == name or key.startswith(name + "."):
                sys.modules.pop(key, None)
    sys.meta_path.insert(0, MockFinder(list(autodoc_mock_imports)))

# ---------------------------------------------------------------------------
# Make the four packages importable from this workspace checkout
# ---------------------------------------------------------------------------


def _bind_flat_package(name: str, root: Path) -> None:
    """Load a setuptools ``package-dir = {name: '.'}`` checkout as ``name``."""
    init = root / "__init__.py"
    if not init.is_file():
        return
    existing = sys.modules.get(name)
    if existing is not None:
        file = getattr(existing, "__file__", None)
        if file and Path(file).resolve().parent == root.resolve():
            return
    spec = importlib.util.spec_from_file_location(
        name,
        init,
        submodule_search_locations=[str(root)],
    )
    if spec is None or spec.loader is None:
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(name, None)
        print(f"docs: skip import {name} from {root}: {exc}", file=sys.stderr)


def _sibling(name: str) -> Path | None:
    for folder in (_WORKSPACE / name, _WORKSPACE / f"{name}-main"):
        if folder.is_dir():
            return folder
    return None


_ffpopt = _sibling("ffpopt")
if _ffpopt is not None:
    _lib = _ffpopt / "src" / "python" / "lib"
    if (_lib / "ffpopt" / "__init__.py").is_file():
        sys.path.insert(0, str(_lib))

for _name in ("ligandparam", "scission", "alps"):
    _root = _sibling(_name)
    if _root is not None:
        _bind_flat_package(_name, _root)

try:
    import alps as _alps_pkg  # noqa: F401  # binds companions if not already
except Exception:
    pass

try:
    from alps import __version__ as release
except Exception:
    release = "unknown"

# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

project = "ALPS"
copyright = "2026, Zeke Piskulich, German P. Barletta, Timothy J. Giese, Nate Levinzon"
author = "Zeke Piskulich, German P. Barletta, Timothy J. Giese, Nate Levinzon"
version = release

# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "gen_api.py", "**/__pycache__"]
source_suffix = {".rst": "restructuredtext"}
root_doc = "index"
language = "en"

# ---------------------------------------------------------------------------
# Autodoc: every function, class, and method (including undocumented)
# ---------------------------------------------------------------------------

autosummary_generate = False
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_preserve_defaults = True
autodoc_inherit_docstrings = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": True,
    "special-members": "__init__",
    "show-inheritance": True,
    "ignore-module-all": True,
    "member-order": "bysource",
    "exclude-members": "__weakref__, __dict__, __module__, __annotations__",
}

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True

todo_include_todos = True

# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "ALPS documentation"
html_short_title = "ALPS"
html_theme_options = {
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
    "logo_only": False,
}
html_context = {
    "display_github": True,
    "github_user": "ndlevinzon",
    "github_repo": "alps-workspace",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
if os.environ.get("READTHEDOCS") == "True":
    html_context["READTHEDOCS"] = True
if os.environ.get("READTHEDOCS_CANONICAL_URL"):
    html_baseurl = os.environ["READTHEDOCS_CANONICAL_URL"]

# ---------------------------------------------------------------------------
# Intersphinx
# ---------------------------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
    "ase": ("https://docs.ase-lib.org/", None),
}

nitpicky = False
suppress_warnings = ["docutils"]


def setup(app):
    """Skip interpreter dunders that autodoc would otherwise list as members."""

    def _skip_member(app, what, name, obj, skip, options):  # noqa: ARG001
        if name in {
            "__weakref__",
            "__dict__",
            "__module__",
            "__annotations__",
            "__orig_bases__",
            "__parameters__",
        }:
            return True
        return skip

    app.connect("autodoc-skip-member", _skip_member)
    return {"parallel_read_safe": True, "parallel_write_safe": True}

