# ALPS workspace

Umbrella checkout for four independent GitHub repos. ALPS orchestrates
ligandparam, scission, and ffpopt; each subdirectory is its own git repo.

| Folder | Package | Remote |
|--------|---------|--------|
| `alps` | `alps` | https://github.com/ndlevinzon/alps |
| `ligandparam` | `ligandparam` | https://github.com/ndlevinzon/ligandparam |
| `scission` | `scission` | https://github.com/ndlevinzon/scission |
| `ffpopt` | `ffpopt` | https://github.com/ndlevinzon/ffpopt |

Open `alps.code-workspace` in Cursor/VS Code so each repo is a named git root.

## Two-push workflow

1. Commit and push inside the tool you edited.
2. In this workspace root, commit the updated submodule pointer and push.

A change that spans two tools is three pushes (both tools, then this workspace).

## Install

See [`alps/README.md`](alps/README.md).
