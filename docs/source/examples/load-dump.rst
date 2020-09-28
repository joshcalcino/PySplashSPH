-------------------
Load a Phantom Dump
-------------------

Load a standard Phantom dump file and access the data arrays.


.. code-block:: python

    import pysplashsph

    dumpfile = 'dump_00000'

    dump = pysplashsph.read.read_data(dumpfile, datatype='Phantom')

    print(dump['x'])
