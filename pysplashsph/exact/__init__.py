"""
The exact sub-package




"""

from ctypes import cdll
from pkg_resources import resource_filename
import sys

try:
    _libexact = cdll.LoadLibrary(resource_filename('pysplashsph', 'libs/libexact.so'))
except OSError:
    print("PySplashSPH ERROR: Could not load `libexact.so`")
    sys.exit(1)

from .exact import (shock, shock_sr, sedov, polytrope,
                    toystar1D, toystar2D, gresho, rhoh,
                    torus, ringspread, dustywave, rochelobe,
                    cshock, planetdisc, bondi)

__all__ = ['shock', 'shock_sr', 'sedov', 'polytrope',
           'toystar1D', 'toystar2D', 'gresho', 'rhoh',
           'torus', 'ringspread', 'dustywave', 'rochelobe',
           'cshock', 'planetdisc', 'bondi']
