"""
PySPLASH
=====
**PySPLASH** is a Python package that provides access to the Fortran
subroutines from the SPH visualisation code SPLASH.
Features
--------
- Plotting exact analytic functions for many hydrodynamical problems
- Reading many SPH code data formats
- Interpolation routines for SPH visualisation
Subpackages
-----------
- exact
    Contains functions for exact solutions to many hydrodynamical
    problems
- read
    Contains functions for reading data formats from many different
    SPH codes
- interpolation
    Contains functions for SPH interpolation
Documentation
-------------
See **** for documentation. The source code is
available at ****.
"""

import logging
import platform
from typing import Any

# Canonical version number
__version__ = '0.0.1'

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('.pysplash.log')

console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

console_format = logging.Formatter('%(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def get_os_info():
    """Get the operating system version for logging."""
    system = platform.system()
    if system == 'Darwin':
        system = 'macOS'
    release = platform.release()
    return f'{system} version: {release}'

logger.debug('PySPLASH v{} on Python {}'.format(__version__, platform.python_version()))
logger.debug('{}, {}'.format(get_os_info(), platform.machine()))

from . import exact, read #, interpolation

__all__ = (['exact', 'read'])
