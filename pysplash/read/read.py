import os.path
from pathlib import Path

from ctypes import c_int, c_float, c_bool, c_double, c_char_p, byref, POINTER, pointer, cast
from . import libread
import copy

import numpy as np


def read_data(filename, filetype, ncol=None, npart=None, verbose=False):

    filename = filename.encode('utf-8')
    filetype = filetype.encode('utf-8')

    f_length = c_int(len(filename))
    ff_length = c_int(len(filetype))

    # set up verbosity
    if verbose:
        verbose_int = c_int(1)
    else:
        verbose_int = c_int(0)

    # We need to know the amount of memory to allocate. If this is not yet
    # given, we need to find out how much to allocate.
    if ncol is None or npart is None:
        # ncol and npart will be obtained from our first call to libread.read_data
        # This first call will not result in the data actually being loaded
        # for some data formats, e.g.
        # Phantom, SPHng, gadget, and others,

        ncol_in = 0
        npart_in = 0

        ncol_in_c = c_int(ncol_in)
        npart_in_c = c_int(npart_in)

        # Fortran subroutine arguments are:
        # filename,fileformat,f_length, ff_length,&
        # sph_dat,npart,ncol,read_header,verbose,ierr

        # Tell ctypes what data types we are going to send to our Fortran code
        libread.read_data.argtypes = \
                [c_char_p, c_char_p, POINTER(c_int), POINTER(c_int),
                 POINTER(c_double * npart_in * ncol_in), POINTER(c_int), POINTER(c_int),
                 POINTER(c_int), POINTER(c_int), POINTER(c_int)]

        sph_dat = (c_double * npart_in * ncol_in)() # Order of npart and ncol matters here

        # Capture error flag with an integer
        ierr = c_int(0)

        # Indicate that we just want to read the header to get ncol and npart
        read_header = c_int(1)

        libread.read_data(c_char_p(filename), c_char_p(filetype),
                          byref(f_length), byref(ff_length),
                          byref(sph_dat),
                          byref(npart_in_c), byref(ncol_in_c),
                          byref(read_header), byref(verbose_int), byref(ierr))


        if verbose: print("Got file size, ncol="+ str(ncol_in_c) +
                            ", npart=" + str(npart_in_c))

        ncol = ncol_in_c
        npart = npart_in_c

    else:
        # If ncol and npart are given, convert to c_int
        npart = c_int(npart)
        ncol = c_int(ncol)

    # Update argtypes based on array size
    libread.read_data.argtypes = \
            [c_char_p, c_char_p, POINTER(c_int), POINTER(c_int),
             POINTER(c_double * npart.value * ncol.value), POINTER(c_int), POINTER(c_int),
             POINTER(c_int), POINTER(c_int), POINTER(c_int)]

    sph_dat = (c_double * npart.value * ncol.value)()

    ierr = c_int(0)
    read_header = c_int(0)

    libread.read_data(c_char_p(filename), c_char_p(filetype), # strings
                          byref(f_length), byref(ff_length), # length of previous strings
                          byref(sph_dat), # An array with the size of the SPH data
                          byref(npart), byref(ncol), # the size of sph_dat
                          byref(read_header), byref(verbose_int), byref(ierr))

    if ierr == 1:
        print("Error")
        exit(1)

    # Turn data into a numpy array
    sph_data = np.ctypeslib.as_array(sph_dat).T

    return sph_data
