import os.path
from pathlib import Path

from ctypes import c_int, c_float, c_bool, c_double, c_char_p, byref, POINTER, pointer, cast
from . import libread
import copy

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

        ncol_in_c = c_int(ncol_in)
        npart_in_c = c_int(npart_in)

        # sph_dat = np.empty((ncol_in, npart_in), dtype=c_double)
        sph_dat = (c_double * ncol_in * npart_in)()

        ierr = 0
        libread.read_data(c_char_p(filename), c_char_p(filetype),
                          byref(c_int(f_length)), byref(c_int(ff_length)),
                          byref(sph_dat),
                          byref(ncol_in_c), byref(npart_in_c), byref(c_int(ierr)))
        print("Got file size, ncol="+ str(ncol_in_c) + ", npart=" + str(npart_in_c))
        ncol = ncol_in_c.value
        npart = npart_in_c.value

    # sph_dat = np.empty((ncol, npart), dtype=c_double)
    print("ncol and npart are " + str(ncol) + "  " + str(npart) + " in Python after\
    converting to python types")

    sph_dat = (c_double * ncol * npart)()

    ierr = 0
    libread.read_data(c_char_p(filename), c_char_p(filetype),
                          byref(c_int(f_length)), byref(c_int(ff_length)),
                          byref(sph_dat),
                          byref(c_int(ncol)), byref(c_int(npart)), byref(c_int(ierr)))

    if ierr == 1:
        print("Error")
        exit(1)

    array_of_size_doubles = c_double*ncol*npart
    buffer_as_ctypes_array = cast(sph_dat, POINTER(array_of_size_doubles))[0]

    sph_data = np.ctypeslib.as_array(buffer_as_ctypes_array)


    return sph_data



def read_data_test(filename, filetype, ncol=None, npart=None):

    filename = filename.encode('utf-8')
    filetype = filetype.encode('utf-8')

    f_length = len(filename)
    ff_length = len(filetype)

    # fd = cdll.LoadLibrary('float.dll')

    # read = libread.read_data_test

# c_char_p(filename), c_char_p(filetype),
#                   byref(c_int(f_length)), byref(c_int(ff_length)),
#                   byref(sph_dat),
#                   byref(ncol_in_c), byref(npart_in_c), byref(c_int(ierr))
#
# filename,fileformat,f_length, ff_length,&
#                        sph_dat,npart,ncol,ierr

    libread.read_data_test.argtypes = [c_char_p, c_char_p, POINTER(c_int), POINTER(c_int),
    POINTER(POINTER(c_double)), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    #
    # libread.read_data_test.restypes = [c_char_p, c_char_p, POINTER(c_int), POINTER(c_int),
    # POINTER(POINTER(c_double)), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

    # sph_dat = POINTER(c_float)()
    # ip = c_int(0)
    # fd.floatarr(pointer(ip),pointer(fpp))

    # We need to know the amount of memory to allocate. If this is not yet
    # given, we need to find out how much to allocate.

    # Eventually we would like to obtain nc, np without loading the data,
    # but need to write the function to do this.
    print("Trying to work out the file size")

    ncol_in = 0
    npart_in = 0

    ncol_in_c = c_int(ncol_in)
    npart_in_c = c_int(npart_in)

    # sph_dat = np.empty((ncol_in, npart_in), dtype=c_double)
    # sph_dat = POINTER(c_double)()

    sph_dat = POINTER(c_double)()
    # sph_dat = np.ctypeslib.ndpointer(flags='F')

    ierr = 0
    libread.read_data_test(c_char_p(filename), c_char_p(filetype),
                      byref(c_int(f_length)), byref(c_int(ff_length)),
                      byref(sph_dat),
                      byref(ncol_in_c), byref(npart_in_c), byref(c_int(ierr)))

    array_of_size_doubles = c_double*ncol_in_c.value*npart_in_c.value
    buffer_as_ctypes_array = cast(sph_dat, POINTER(array_of_size_doubles))[0]
    buffer_as_numpy_array = np.frombuffer(buffer_as_ctypes_array, np.float)
    # a = numpy.frombuffer(buffer, float)

    # list_of_results = sph_dat[:ncol_in_c.value*npart_in_c.value]
    sph_data = np.resize(buffer_as_numpy_array, (npart_in_c.value, ncol_in_c.value))
    sph_data2 = np.ctypeslib.as_array(buffer_as_ctypes_array)

    print(buffer_as_ctypes_array)
    print(buffer_as_ctypes_array[10][10000])
    # print(buffer_as_numpy_array[10, 10000])
    print(sph_data[10, 10000])
    print(sph_data2[10, 10000])
    # print(buffer_as_numpy_array)

    print("Got file size, ncol="+ str(ncol_in_c) + ", npart=" + str(npart_in_c))
    ncol = ncol_in_c.value
    npart = npart_in_c.value
    print("reset ncol and npart")



    if ierr == 1:
        print("Error")
        exit(1)

    sph_data = copy.deepcopy(sph_data2)


    return sph_data
