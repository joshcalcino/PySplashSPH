import pysplash
import numpy as np
import os

test_dir = os.path.dirname(os.path.realpath(__file__))
test_file_ascii  = os.path.join(test_dir, 'test_00000.ascii')
test_file_binary = os.path.join(test_dir, 'test_00000')

def test_read(capfd):

    print("Loading:",test_file_ascii)
    sph_data_from_ascii = np.genfromtxt(test_file_ascii)

    print("Loading:",test_file_binary)
    dump = pysplash.read.read_data(test_file_binary, filetype='Phantom')
    sph_data = dump.data

    capfd.readouterr()  # capture OS level output, so that it can be silenced with "pytest -s"

    # Don't check if they are exactly equal, since ascii data is rounded
    if np.allclose(sph_data_from_ascii, sph_data):
        success = True
    else:
        success = False
        print("\nERROR in loading data!\n")
        print("\nFirst 5 rows of sph_data")
        print(sph_data[0:5])
        print("\nFirst 5 rows of sph_data_from_ascii")
        print(sph_data_from_ascii[0:5])
        print("\nLast 5 rows of sph_data")
        print(sph_data[-5:])
        print("\nLast 5 rows of sph_data_from_ascii")
        print(sph_data_from_ascii[-5:])

    assert success, 'Binary data does not match ascii data.'
