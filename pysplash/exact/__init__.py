""" The exact sub-package


"""

from ctypes.utils import find_library
from ctypes import LibraryLoader, cdll

_libexactpath = find_library("libexact")

if _libexactpath is None:
    print("Could not find `libexact.so`")
    print("Please update your PATH")
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
