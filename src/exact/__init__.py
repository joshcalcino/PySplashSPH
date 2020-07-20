""" The exact sub-package


"""

from ctypes import LibraryLoader, cdll
from pkg_resources import resource_filename
import os
import sys


try:
    libexact = cdll.LoadLibrary(resource_filename(__name__, 'libs/libexact.so'))
except OSError:
    print("PySPLASH ERROR: Could not load `libexact.so`")
    sys.exit(1)

from .exact import (shock, shock_sr, sedov, polytrope,
                    toystar1D, toystar2D, gresho, rhoh,
                    torus, ringspread, dustywave, rochelobe,
                    cshock, planetdisc, bondi)

__all__ = ['shock', 'shock_sr', 'sedov', 'polytrope',
           'toystar1D', 'toystar2D', 'gresho', 'rhoh',
           'torus', 'ringspread', 'dustywave', 'rochelobe',
           'cshock', 'planetdisc', 'bondi']
