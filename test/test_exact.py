import pysplash
import numpy as np

x = np.linspace(0, 1, 10)

x, y, ierr = pysplash.exact.shock(x)
