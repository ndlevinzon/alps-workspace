Developer guide
===============

.. todo:: Write the developer guide: checkout layout, editable installs,
   running tests, adding a stage or workflow, stdout/logging rules, and
   how to refresh this Sphinx tree (``python docs/gen_api.py``).

Until that lands, see the ALPS README and :doc:`../companions`.

Read the Docs
-------------

The combined site is built from the **workspace** repo
(``ndlevinzon/alps-workspace``), not from the individual tool remotes.

1. Import that GitHub repo at https://readthedocs.org/ (slug
   ``alps-workspace`` if you want the README badge to resolve).
2. The build file is ``.readthedocs.yaml`` at the workspace root: Ubuntu
   24.04, Python 3.12, recursive submodules, ``docs/requirements.txt``,
   then ``python docs/gen_api.py`` before Sphinx.
3. Do not pip-install ``ffpopt-main`` on RTD (CMake). ``docs/conf.py``
   adds ``ffpopt-main/src/python/lib`` to ``sys.path``.
4. Optional science stacks (rdkit, ParmEd, MDAnalysis, geomeTRIC, tblite,
   ...) are mocked when they are not installed, so the API pages still
   build.
