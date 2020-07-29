""" The read sub-package

This sub-package will read many different SPH data formats, and return
their contents as a numpy array

"""

from ctypes.util import find_library
from ctypes import LibraryLoader, cdll
import os

_libreadpath = find_library("libread")

if _libreadpath is None:
    try:
        HOME = os.environ['HOME']
        _libreadpath = os.path.join(HOME, 'splash/build/libread.so')
        libread = cdll.LoadLibrary(_libreadpath)
    except OSError:
        try:
            SPLASH_DIR = os.environ['SPLASH_DIR']
            _libereadpath = os.path.join(str(SPLASH_DIR), 'build/libread.so')
            libread = cdll.LoadLibrary(_libreadpath)
        except KeyError or OSError:
            print("PySPLASH ERROR: Could not find `libread.so`")
            print("Please make sure that you have SPLASH installed.")
            print("If you do not have admin privledges, please set an")
            print("environment variable `SPLASH_DIR` that points to the")
            print("directory where SPLASH is located.")
            exit(1)
else:
    libread = cdll.LoadLibrary(str(_libreadpath))
    libread.check_argcv_f()


from .read import read_data, read_data_test

__all__ = ['read_data', 'read_data_test']
