import pysplash
import numpy as np

print("Loading data from ascii, this might take a while..")
sph_data_from_ascii = np.genfromtxt('/home/josh/pysplash/test/test_00000.ascii')

# sph_data_from_ascii includes an extra column that is not in sph_dat, so ignore
sph_data_from_ascii = sph_data_from_ascii[:, :-1]

print("Loading binary data from Fortran, this should be much faster!")
sph_data = pysplash.read.read_data('/home/josh/pysplash/test/test_00000', 'phantom')

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
