import pysplash
import numpy as np
import os

test_dir = os.path.dirname(os.path.realpath(__file__))
test_file_ascii  = os.path.join(test_dir, 'test_00000.ascii')
test_file_binary = os.path.join(test_dir, 'test_00000')

print("Loading data from ascii, this might take a while..")
sph_data_from_ascii = np.genfromtxt(test_file_ascii)

print("Loading binary data from Fortran, this should be much faster!")
dump = pysplash.read.read_data(test_file_binary, filetype='Phantom')

sph_data = dump.data

# Don't check if they are exactly equal, since ascii data is rounded
if np.allclose(sph_data_from_ascii, sph_data):
    print("Data loaded successfully")

else:
    print("ERROR in loading data!")

    print("\n \n")

    print("Here are the first 5 rows of sph_data")
    print(sph_data[0:5])

    print("\n \n")

    print("Here are the first 5 rows of sph_data_from_ascii")
    print(sph_data_from_ascii[0:5])

    print("\n \n")

    print("Here are the last 5 rows of sph_data")
    print(sph_data[-5:])

    print("\n \n")

    print("Here are the last 5 rows of sph_data_from_ascii")
    print(sph_data_from_ascii[-5:])
    exit(1)
