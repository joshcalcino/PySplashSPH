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

Note that this will automatically build the `splash` libraries and copy them into the correct location (`pysplash/libs/.`), however it will not "audit" or "delocate" the wheel (i.e. copy in and relink any non-standard external libraries that are dependencies).

To build a 'fixed' wheel instead, run the script `build-wheels.sh`, which will build as well as audit the wheel for you. Fixed wheels are stored in `pysplash/wheelhouse`. You can choose to install directly from a wheel with `pip install <wheel-name>.whl`.

### Search paths
`setup.py` will search for an installation of Splash in the following directories, in this order:

1. In the current directory, i.e.
   ```
   pysplash/
      |--- README.md
      |--- pysplash/
      |--- setup.py
        ...
      |--- splash/
      ...
      |--- test/
      |--- wheelhouse/
   ```
2. In the parent directory, i.e.
   ```
   splash/
      |--- bin/
      |--- build/
        ...
      |--- pysplash/
      ...
      |--- src/
   ```
3. In the directory defined by the environment variable `$SPLASH_DIR`
4. In `$HOME/splash`
