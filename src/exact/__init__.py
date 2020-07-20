""" The exact sub-package


"""

from ctypes import LibraryLoader, cdll
import os


try:
    HOME = os.environ['HOME']
    _libexactpath = os.path.join(HOME, 'splash/build/libexact.so')
    libexact = cdll.LoadLibrary(_libexactpath)
except OSError:
    try:
        SPLASH_DIR = os.environ['SPLASH_DIR']
        _libexactpath = os.path.join(str(SPLASH_DIR), 'build/libexact.so')
        libexact = cdll.LoadLibrary(_libexactpath)
    except KeyError or OSError:
        print("PySPLASH ERROR: Could not find `libexact.so`")
        print("Please make sure that you have SPLASH installed.")
        print("If you do not have admin privledges, please set an")
        print("environment variable `SPLASH_DIR` that points to the")
        print("directory where SPLASH is located.")
        exit(1)


from .exact import (shock, shock_sr, sedov, polytrope,
                    toystar1D, toystar2D, gresho, rhoh,
                    torus, ringspread, dustywave, rochelobe,
                    cshock, planetdisc, bondi)

__all__ = ['shock', 'shock_sr', 'sedov', 'polytrope',
           'toystar1D', 'toystar2D', 'gresho', 'rhoh',
           'torus', 'ringspread', 'dustywave', 'rochelobe',
           'cshock', 'planetdisc', 'bondi']
