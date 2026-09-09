#!/usr/bin/env python3
"""Write one automodule RST page per Python module in the four packages.

Run from the workspace root or from ``docs/``::

    python docs/gen_api.py
    python gen_api.py
"""

from __future__ import annotations

from pathlib import Path

_DOCS = Path(__file__).resolve().parent
_WORKSPACE = _DOCS.parent

_SKIP_DIR_NAMES = {
    "tests",
    "docs",
    "pkgdata",
    "__pycache__",
    ".git",
    "ligandparam.egg-info",
    "scission.egg-info",
    "alps.egg-info",
    "ffpopt.egg-info",
}

_PACKAGES = (
    ("alps", None, "ALPS"),
    ("ligandparam", None, "LigandParam"),
    ("scission", None, "Scission"),
    ("ffpopt", None, "FFPOPT"),
)


def _sibling(name: str) -> Path | None:
    for folder in (_WORKSPACE / name, _WORKSPACE / f"{name}-main"):
        if folder.is_dir():
            return folder
    return None


def _package_root(name: str, explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit
    sibling = _sibling(name)
    if sibling is None:
        raise FileNotFoundError(f"No checkout for {name} beside {_WORKSPACE}")
    if name == "ffpopt":
        lib = sibling / "src" / "python" / "lib" / "ffpopt"
        if (lib / "__init__.py").is_file():
            return lib
    if (sibling / "__init__.py").is_file():
        return sibling
    raise FileNotFoundError(f"Cannot find {name} package root under {sibling}")


def _iter_modules(package: str, root: Path) -> list[str]:
    names = [package]
    for path in sorted(root.rglob("*.py")):
        if any(part in _SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.name.startswith("test_"):
            continue
        rel = path.relative_to(root)
        if rel.name == "__init__.py":
            if rel.parent == Path("."):
                continue
            parts = list(rel.parent.parts)
        else:
            parts = list(rel.with_suffix("").parts)
        if any(part in _SKIP_DIR_NAMES for part in parts):
            continue
        names.append(".".join((package, *parts)))
    return names


def _underline(title: str, char: str = "=") -> str:
    return f"{title}\n{char * len(title)}"


def _module_page(fullname: str) -> str:
    return (
        f"{_underline(fullname)}\n"
        f"\n"
        f".. automodule:: {fullname}\n"
        f"\n"
    )


def _package_index(title: str, package: str, modules: list[str]) -> str:
    entries = "\n".join(f"   {name}" for name in modules)
    return (
        f"{_underline(f'{title} API reference')}\n"
        f"\n"
        f"Complete autodoc of every module, class, function, and method in\n"
        f"``{package}`` (including private and undocumented members).\n"
        f"\n"
        f".. toctree::\n"
        f"   :maxdepth: 1\n"
        f"\n"
        f"{entries}\n"
    )


def main() -> None:
    api = _DOCS / "api"
    for package, explicit, title in _PACKAGES:
        root = _package_root(package, explicit)
        modules = _iter_modules(package, root)
        dest = api / package
        dest.mkdir(parents=True, exist_ok=True)
        for old in dest.glob("*.rst"):
            old.unlink()
        (dest / "index.rst").write_text(
            _package_index(title, package, modules), encoding="utf-8"
        )
        for name in modules:
            (dest / f"{name}.rst").write_text(_module_page(name), encoding="utf-8")
        print(f"{package}: {len(modules)} modules -> {dest}")


if __name__ == "__main__":
    main()
