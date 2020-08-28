""" The interpolation sub-package


"""

from ctypes.util import find_library
from ctypes import LibraryLoader, cdll
import os

_libinterpolationpath = find_library("libexact")

if _libinterpolationpath is None:
    try:
        HOME = os.environ['HOME']
        _libinterpolationpath = os.path.join(HOME, 'splash/build/libinterpolation.so')
        libinterpolation = cdll.LoadLibrary(_libinterpolationpath)
    except OSError:
        try:
            SPLASH_DIR = os.environ['SPLASH_DIR']
        except KeyError:
            print("PySPLASH ERROR: Could not find `libinterpolation.so`")
            print("Please make sure that you have SPLASH installed.")
            print("If you do not have admin privledges, please set an")
            print("environment variable `SPLASH_DIR` that points to the")
            print("directory where SPLASH is located.")
            exit(1)
else:
    libinterpolation = cdll.LoadLibrary(str(_libinterpolationpath))
    libinterpolation.check_argcv_f()

from .interpolation import (shock, shock_sr, sedov, polytrope,
                    toystar1D, toystar2D, gresho, rhoh,
                    torus, ringspread, dustywave, rochelobe,
                    cshock, planetdisc, bondi)

__all__ = ['shock', 'shock_sr', 'sedov', 'polytrope',
           'toystar1D', 'toystar2D', 'gresho', 'rhoh',
           'torus', 'ringspread', 'dustywave', 'rochelobe',
           'cshock', 'planetdisc', 'bondi']
