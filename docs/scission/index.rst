Scission
========

Scission builds AMBER-aware torsion fragments from a charged ligand triplet
(``.mol2`` / ``.lib`` / ``.frcmod``). It enumerates acyclic rotatable bonds,
caps and reduces fragments, writes scan-ready Amber files, and merges
fitted ``DIHE`` terms back into the parent ``frcmod``.

ALPS ``lig-scission`` and the default ``lig-dihed-correct`` path call this
package. Choose a scheme with ``--strategy scission`` (default), ``pfizer``,
or ``wbo`` **before** the ffpopt dihedral scan. The ``scission`` console
script is the scission package itself.

Python::

    from scission import fragment_ligand
    from scission.Merge import merge_fragment_frcmods

Package layout
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Role
   * - :mod:`scission.Pipeline`
     - ``fragment_ligand`` entry point
   * - :mod:`scission.Models`
     - Ligand / fragment / torsion dataclasses
   * - :mod:`scission.Graph`
     - Bond graph and rotatable-bond enumeration
   * - :mod:`scission.Capping`
     - Caps and reduced fragments
   * - :mod:`scission.Torsions`
     - Torsion definitions and SMARTS matching
   * - :mod:`scission.Strategies`
     - Named schemes (``scission``, ``pfizer``, ``wbo``) plus user registration
   * - :mod:`scission.Merge`
     - Splice fragment ``DIHE`` into the parent frcmod
   * - :mod:`scission.Cli`
     - ``scission fragment`` / ``merge`` / ``pick-bond``

The complete member list is in the :doc:`../api/scission/index`.
