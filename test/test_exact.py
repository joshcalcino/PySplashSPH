import pysplash
import numpy as np

def test_shock(capfd):
  x = np.linspace(0, 1, 10)
  y = pysplash.exact.shock(x)
  capfd.readouterr()  # capture OS level output, so that it can be silenced with "pytest -s"
