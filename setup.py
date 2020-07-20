"""PySPLASH setup.py."""

import io
import pathlib
import re

from setuptools import setup

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open('src/__init__.py', encoding='utf_8_sig').read(),
).group(1)

install_requires = [
    'numpy',
    'pandas',
    'pint>=0.10.1',
    'scipy',
    'tqdm',
]
packages = [
    'pysplash',
    'pysplash.exact',
    # 'pysplash.read'
]

package_dir = {'pysplash' : 'src'}

description = 'Python wrapper module around SPLASH utilities.'
long_description = (pathlib.Path(__file__).parent / 'README.md').read_text()

setup(
    name='pysplash',
    version=__version__,
    author='Josh Calcino',
    author_email='josh.calcino@gmail.com',
    url='https://github.com/joshcalcino/PySPLASH',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=packages,
    package_dir=package_dir,
    license='MIT',
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Mac, Linux",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
