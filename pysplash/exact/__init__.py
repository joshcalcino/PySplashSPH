""" The exact sub-package


"""

from ctypes.utils import find_library
from ctypes import LibraryLoader, cdll

from .exact import *

libexactpath = find_library("libexact")

if libexactpath is None:
    print("Could not find `libexact.so`")
    print("Please update your PATH")
    exit(1)
else:
    _exactlib = cdll.LoadLibrary(str(libexactpath))
    _exactlib.check_argcv_f()
