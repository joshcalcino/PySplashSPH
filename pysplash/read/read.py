import os.path
from pathlib import Path

from ctypes import c_int, c_float, c_bool, c_double, c_char_p, byref, POINTER
from . import libread

import numpy as np


def read_data(filename, filetype, ncol=None, npart=None):

    filename = filename.encode('utf-8')
    filetype = filetype.encode('utf-8')

    f_length = len(filename)
    ff_length = len(filetype)

    # We need to know the amount of memory to allocate. If this is not yet
    # given, we need to find out how much to allocate.
    if ncol is None or npart is None:
        # Eventually we would like to obtain nc, np without loading the data,
        # but need to write the function to do this.
        print("Trying to work out the file size")

        ncol_in = 0
        npart_in = 0

        sph_dat = np.empty((ncol_in, npart_in), dtype=c_double)

        ierr = 0
        libread.read_data(c_char_p(filename), c_char_p(filetype),
                          byref(c_int(f_length)), byref(c_int(ff_length)),
                          sph_dat.ctypes.data_as(POINTER(c_double)),
                          byref(c_int(ncol_in)), byref(c_int(npart_in)), byref(c_int(ierr)))
        print("Got file size, ncol="+ str(ncol_in) + ", npart=" + str(npart_in))
        ncol = ncol_in
        npart = npart_in

    sph_dat = np.empty((ncol, npart), dtype=c_double)

    ierr = 0
    libread.read_data(c_char_p(filename), c_char_p(filetype),
                          byref(c_int(f_length)), byref(c_int(ff_length)),
                          byref(sph_dat.ctypes.data_as(POINTER(c_double))),
                          byref(c_int(ncol)), byref(c_int(npart)), byref(c_int(ierr)))

    if ierr == 1:
        print("Error")
        exit(1)

    return sph_dat
