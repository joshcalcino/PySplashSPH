PySPLASH
========

Smoothed particle hydrodynamics stuff.

---

## Building/Installing from source
Installing from source requires an installation of Splash. To install:
```
python setup.py install
```

To build a python wheel:
```
python setup.py bdist_wheel
```

`setup.py` will search for and installation of Splash in the following directories in this order:

1. In the parent directory. (i.e. the `pysplash` source is with `splash`)
   ```
   splash/
      |--- bin/
      |--- build/
        ...
      |--- pysplash/
   ```
2. In the directory defined by the environment variable `$SPLASH_DIR`
3. In `$HOME/splash`
