PySplashSPH
========

A Python wrapper for the smoothed particle hydrodynamics plotting library SPLASH.
Currently supports reading many SPH data formats, and useful exact analytic solutions
for specific hydrodynamics problems.

PySplashSPH currently does not wrap the SPLASH interpolation routines, however this
is planned for a future release.

[![Build Status](https://travis-ci.com/joshcalcino/pysplashsph.svg?branch=master)](https://travis-ci.com/github/joshcalcino/pysplashsph)
[![Documentation Status](https://readthedocs.org/projects/pysplash/badge/?version=latest)](https://pysplash.readthedocs.io/en/latest/?badge=latest)


---

## Building/Installing from source
**Note: installing PySlashSPH from source requires a local installation of Splash.**

Clone the repository and navigate to the directory
```
git clone --recursive https://github.com/joshcalcino/PySplashSPH.git
cd PySplashSPH
```
Adding `--recursive` ensures that you have an installation of Splash by populating the git submodule.

Run `setup.py` to install:
```
python setup.py install
```

Or, you can choose to build and install a python wheel
```
python setup.py bdist_wheel
pip install dist/<name-of-wheel>.whl
```

`setup.py` will automatically build the Fortran `splash` libraries and copy them into the correct location (`pysplashsph/libs/.`). See below for the list of paths searched for an installation of Splash.

Note that when building a wheel, it will not be "audited" or "delocated" i.e. the wheel may have dependencies on external libraries that are non-standard. See PEP [513](https://www.python.org/dev/peps/pep-0513/), [571](https://www.python.org/dev/peps/pep-0571/) and [599](https://www.python.org/dev/peps/pep-0571/).
This is not an issue unless you wish to distribute the wheel and/or install it on a different machine.

To build a 'fixed' wheel instead, run the script `build-wheels.sh`, which will build as well as audit the wheel for you. Fixed wheels are stored in `pysplashsph/wheelhouse/`.

### Search paths
`setup.py` will search for an installation of Splash in the following directories, in this order:

1. In the current directory, i.e.
   ```
   PySplashSPH/
      |--- README.md
      |--- pysplashsph/
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
      |--- PySplashSPH/
      ...
      |--- src/
   ```
3. In the directory defined by the environment variable `$SPLASH_DIR`
4. In `$HOME/splash`

Note that unless you cloned the repository with the `--recursive` flag, the splash git submodule will not be populated, meaning option 1 will be skipped and `setup.py` will look for an installation of splash in the other locations.
