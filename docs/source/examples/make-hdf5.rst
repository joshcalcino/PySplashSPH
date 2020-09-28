--------------------------
Create an HDF5 File Object
--------------------------

A binary dump file can be loaded using PySplashSPH and then converted into
an HDF5 File object. The object can be used to interact with external modules,
such as `Plonk <https://plonk.readthedocs.io/en/stable/>`_.

.. note::

    Loading a binary file and converting to an HDF5 file is filetype dependent.
    For example, a Phantom dump file converted to an HDF5 File object will have
    different HDF5 groups than a non-Phantom HDF5 File object. This is so that
    the Phantom HDF5 File object can be used as an input to Plonk.


.. code-block:: python

    import pysplashsph
    import plonk

    dumpfile = 'dump_00000'

    dump = pysplashsph.read.read_data(dumpfile, datatype='Phantom')

    dump_hdf5 = dump.as_hdf5()

    snap = plonk.load_snap(dump_hdf5)

    snap.image(
      quantity='density',
      x='x',
      y='z',
      interp='slice',
      cmap='gist_heat',
    )
