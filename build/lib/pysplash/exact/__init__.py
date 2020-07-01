""" The exact sub-package


"""

from ctypes.util import find_library
from ctypes import LibraryLoader, cdll
import os

_libexactpath = find_library("libexact")

if _libexactpath is None:
    try:
        HOME = os.environ['HOME']
        _libexactpath = os.path.join(HOME, 'splash/build/libexact.so')
        exactlib = cdll.LoadLibrary(_libexactpath)
        print(exactlib)
    except OSError:
        try:
            SPLASH_DIR = os.environ['SPLASH_DIR']
        except KeyError:
            print("PySPLASH ERROR: Could not find `libexact.so`")
            print("Please make sure that you have SPLASH installed.")
            print("If you do not have admin privledges, please set an")
            print("environment variable `SPLASH_DIR` that points to the")
            print("directory where SPLASH is located.")
            exit(1)
else:
    exactlib = cdll.LoadLibrary(str(_libexactpath))
    exactlib.check_argcv_f()

from .exact import (shock, shock_sr, sedov, polytrope,
                    toystar1D, toystar2D, gresho, rhoh,
                    torus, ringspread, dustywave, rochelobe,
                    cshock, planetdisc, bondi)

__all__ = ['shock', 'shock_sr', 'sedov', 'polytrope',
           'toystar1D', 'toystar2D', 'gresho', 'rhoh',
           'torus', 'ringspread', 'dustywave', 'rochelobe',
           'cshock', 'planetdisc', 'bondi']
