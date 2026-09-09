LigandParam
===========

LigandParam is a stage-based toolkit for Amber parameterization of
nonstandard ligands and residues. Recipes assemble a pipeline
(Antechamber → Gaussian ESP / RESP → ``parmchk2`` → LEaP). Each stage is
one tool step that can be added, removed, or replaced.

ALPS ``lig-getparam`` is a wrapper around the ligandparam CLI. Standalone
ligandparam still ships ``lig-getparam``, ``lighfix``, ``smiles-to-pdb``,
and ``lig-to-sage``.

Recipes
-------

Import from :mod:`ligandparam.recipes` (lazy exports)::

    from ligandparam.recipes import LazyLigand, FreeLigand

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Recipe
     - Typical use
   * - ``LazyLigand``
     - Gaussian min + single-orientation RESP
   * - ``FreeLigand``
     - Multi-orientation RESP
   * - ``LazierLigand``
     - BCC / Antechamber charges, no Gaussian
   * - ``SQMLigand``
     - SQM geometry, BCC charges
   * - ``DPLigand``
     - DeepMD minimize, then Lazy-style RESP
   * - ``DPFreeLigand``
     - DeepMD minimize, then Free-style RESP

Package layout
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Role
   * - :mod:`ligandparam.recipes`
     - Named parameterization pipelines
   * - :mod:`ligandparam.stages`
     - One-tool pipeline steps
   * - :mod:`ligandparam.io`
     - Amber / Gaussian / SMILES I/O
   * - :mod:`ligandparam.multiresp`
     - Multi-orientation RESP helpers
   * - :mod:`ligandparam.runtime`
     - Console boards, CPU budget
   * - :mod:`ligandparam.cli`
     - Standalone console scripts

The complete member list is in the :doc:`../api/ligandparam/index`.
