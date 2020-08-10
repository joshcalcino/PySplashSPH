import os.path
from pathlib import Path

from ctypes import (c_int, c_float, c_bool, c_double, c_char_p,
                        byref, POINTER, pointer, cast, c_char)
from . import _libread as libread

import numpy as np
# from pandas import DataFrame


class DumpFile:
    """PySPLASH dumpfile object. Contains SPH data, labels, units, and other
    attributes.


    """

    def __init__(self):
        self.filepath = None
        self.filetype = None
        self.data = None
        self.labels = []
        self.headers = {}




def get_labels(ncol):
    if type(ncol) is c_int:
        ncol_py = ncol.value

    elif type(ncol) is int:
        ncol_py = ncol
        ncol = c_int(ncol)

    labels = (c_char * 24 * ncol_py)()

    libread.get_labels.argtypes = [POINTER(c_char * 24 * ncol_py), POINTER(c_int)]

    libread.get_labels(byref(labels), byref(ncol))

    labels = [str(labels[i].value.rstrip(), 'utf-8') for i in range(0, ncol.value)]

    return labels

def get_headers():

    headerval_length = c_int()
    headertag_length = c_int()

    libread.get_header_vals_size.argtypes = [POINTER(c_int), POINTER(c_int)]

    libread.get_header_vals_size(byref(headertag_length), byref(headerval_length))

    headertags = (c_char * 24 * headertag_length.value)()
    headervals = (c_double * headerval_length.value)()

    libread.get_headers.argtypes = [POINTER(c_char * 24 * headertag_length.value),
                                    POINTER(c_double * headerval_length.value),
                                    POINTER(c_int), POINTER(c_int)]

    libread.get_headers(byref(headertags), byref(headervals),
                        byref(headertag_length), byref(headerval_length))

    headertags = [str(headertags[i].value.rstrip(), 'utf-8')
                    for i in range(0, headertag_length.value)]

    headervals = np.ctypeslib.as_array(headervals)

    headertags_clean = list()
    headervals_clean = list()

    for i, headertag in enumerate(headertags):
        if headertag != '':
            headertags_clean.append(headertag)
            headervals_clean.append(headervals[i])

    return headertags_clean, headervals_clean

def read_data(filepath, filetype, ncol=None, npart=None, verbose=False):

    if not os.path.exists(filepath):
        raise FileNotFoundError

    filepath = filepath.encode('utf-8')
    filetype = filetype.encode('utf-8')

    f_length = c_int(len(filepath))
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

        libread.read_data(c_char_p(filepath), c_char_p(filetype),
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

    print(npart.value, ncol.value)

    sph_dat = (c_double * npart.value * ncol.value)()

    ierr = c_int(0)
    read_header = c_int(0)

    libread.read_data(c_char_p(filepath), c_char_p(filetype), # strings
                          byref(f_length), byref(ff_length), # length of previous strings
                          byref(sph_dat), # An array with the size of the SPH data
                          byref(npart), byref(ncol), # the size of sph_dat
                          byref(read_header), byref(verbose_int), byref(ierr))

    if ierr == 1:
        print("Error")
        exit(1)

    # Turn data into a numpy array
    sph_data = np.ctypeslib.as_array(sph_dat).T

    labels = get_labels(ncol.value-1)
    labels.append("iamtype") # Last column is always particle type
    header_tags, header_vals = get_headers()

    dump = DumpFile()
    dump.filepath = filepath
    dump.filetype = filetype
    dump.data = sph_data
    dump.headers = dict(zip(header_tags, header_vals))
    dump.labels = labels

    return dump
