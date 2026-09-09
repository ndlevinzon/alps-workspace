FFPOPT
=======

FFPOPT (force-field parameter optimizer) runs high-level geometry
optimizations, wavefront dihedral scans, and torsion fits against a
reference (QM or ML). ALPS calls
:func:`ffpopt.Workflows.run_dihed_twist_workflow` in-process after scission
(or on the intact parent for ``--whole-ligand``).

York also maintains a standalone Sphinx site for ffpopt. This section is
the **full Python API** of the checkout ALPS binds, including modules that
are not listed on that site.

Package layout
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Role
   * - :mod:`ffpopt.Workflows`
     - In-process dihedral-twist + fit orchestration
   * - :mod:`ffpopt.WaveFront`
     - 1-D wavefront scans
   * - :mod:`ffpopt.WaveFrontND`
     - N-D wavefront
   * - :mod:`ffpopt.Dihedrals`
     - Torsion parameter types and fitting helpers
   * - :mod:`ffpopt.GeomOpt`
     - Geometry optimization (ASE / geomeTRIC)
   * - :mod:`ffpopt.ScanAnalysis`
     - HL vs MM comparison plots
   * - :mod:`ffpopt.AmberParm`
     - Amber topology helpers
   * - :mod:`ffpopt.ase`
     - ASE calculators (sander, xtb, ML models, ...)
   * - :mod:`ffpopt.confsearch`
     - Conformer search
   * - :mod:`ffpopt.cpefit`
     - Charge / ESP fitting
   * - :mod:`ffpopt.scosmo`
     - COSMO surface helpers

The complete member list is in the :doc:`../api/ffpopt/index`.
