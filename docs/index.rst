ALPS documentation
==================

**Amber Ligand Parameters (ALPS)** is the orchestrator for three independent
science packages. This site is the combined API reference. Higher-level
writing (developer guide, design philosophy, tutorials) will be added
later under :doc:`guide/index`.

.. toctree::
   :maxdepth: 2
   :caption: ALPS

   alps/index
   companions
   api/alps/index

.. toctree::
   :maxdepth: 2
   :caption: LigandParam

   ligandparam/index
   api/ligandparam/index

.. toctree::
   :maxdepth: 2
   :caption: Scission

   scission/index
   api/scission/index

.. toctree::
   :maxdepth: 2
   :caption: FFPOPT

   ffpopt/index
   api/ffpopt/index

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guide/index

The four packages
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Package
     - Role
   * - ALPS
     - CLI wrappers, logging, and workflow glue. No science of its own.
   * - LigandParam
     - Stage-based Amber parameterization (charges, types, ``lib`` / ``frcmod``).
   * - Scission
     - Torsion fragments from a charged ligand triplet; merge fitted ``DIHE``.
   * - FFPOPT
     - High-level scans, wavefront dihedral twist, and torsion fitting.


ALPS is the only package that imports both scission and ffpopt. scission
must not import ffpopt, ligandparam, or alps. ffpopt must not import
ligandparam or alps.

Building these pages
---------------------

Hosted on Read the Docs:
https://alps-workspace.readthedocs.io/en/latest/

From the workspace root (this repo, with the four package checkouts as
submodules)::

    pip install -r docs/requirements.txt
    cd docs
    python gen_api.py
    sphinx-build -b html . _build/html

On Windows, ``docs\make.bat html`` is equivalent. Open
``docs/_build/html/index.html``.

``gen_api.py`` refreshes one automodule page per Python module. Re-run it
when you add or rename modules. Read the Docs runs the same command from
``.readthedocs.yaml`` on every build. AmberTools, rdkit, and the ffpopt
CMake extension are not required: missing optional imports are mocked.
