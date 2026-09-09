ALPS
====

ALPS binds independent checkouts of ligandparam, scission, and ffpopt and
runs the parameterization / fragmentation / torsion-fit pipeline in one
process. It does not reimplement those tools.

Typical CLIs:

* ``lig-getparam`` — ligandparam recipes (charges, types, baseline Amber triplet)
* ``lig-scission`` — inspect-only fragmentation, or merge
* ``lig-dihed-correct`` — fragment twist (default) or whole-ligand twist, then ffpopt fit

``lig-dihed-correct --strategy`` (and the same flag on ``lig-scission fragment``)
selects the scission scheme **before** the ffpopt scan: ``scission`` (default
rigid-domain shells), ``pfizer``, or ``wbo``. YAML is ``--fragment-config``.
``--whole-ligand`` skips scission, so ``--strategy`` is ignored.

Python entry points live in :mod:`alps.workflows`:

* :func:`alps.workflows.run_fragmented_dihed_twist_workflow`
* :func:`alps.workflows.run_whole_ligand_dihed_twist_workflow`

Package layout
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Role
   * - :mod:`alps.cli`
     - Console scripts (banner, argument parsing, dispatch)
   * - :mod:`alps.workflows`
     - Fragmented and whole-ligand twist orchestration
   * - :mod:`alps.stages`
     - Ligandparam-style stage wrapping the twist workflows
   * - :mod:`alps.companions`
     - Sibling / path / installed companion discovery
   * - :mod:`alps.Log`
     - Shared stdout tee for companion loggers
   * - :mod:`alps.Progress`
     - Live ASCII boards for long twist jobs
   * - :mod:`alps.ffpopt_bridge`
     - In-process ffpopt PrepareInput / option mapping

The complete member list is in the :doc:`../api/alps/index`.

How companions are bound is documented in :doc:`../companions`.
