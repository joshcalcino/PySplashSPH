"""
The read sub-package

This sub-package will read many different SPH data formats, and return
their contents as a numpy array

"""

from ctypes import cdll
from pkg_resources import resource_filename
import sys

try:
    _libread = cdll.LoadLibrary(resource_filename('pysplash', 'libs/libread.so'))
except OSError:
    print("PySPLASH ERROR: Could not load `libread.so`")
    sys.exit(1)

from .read import read_data

__all__ = ['read_data']
