"""PySPLASH setup.py."""

import io
import pathlib
import re
import os
import inspect
import subprocess
import pathlib

from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from wheel.bdist_wheel import bdist_wheel

src_dir = 'pysplash'

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open(os.path.join(src_dir,'__init__.py'), encoding='utf_8_sig').read(),
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
    'pysplash.read'
]

package_dir = {'pysplash': src_dir}
package_data = {"pysplash": ["libs/*.so*", "libs/*.dylib*"]}

description = 'Python wrapper module around SPLASH utilities.'
long_description = (pathlib.Path(__file__).parent / 'README.md').read_text()


def get_splash_dir():
    """
    Locate splash installation.

    Locations are checked in this order:
    1) Parent directory
    2) Environment variable $SPLASH_DIR
    3) $HOME/splash
    """
    parent_dir  = pathlib.Path(os.path.abspath(__file__)).parent.parent
    home_splash = os.path.join(os.environ['HOME'], 'splash')

    if 'splash' == os.path.basename(parent_dir):
        splash_dir = parent_dir
    elif 'SPLASH_DIR' in os.environ:
        splash_dir = os.environ['SPLASH_DIR']
    elif os.path.isdir(home_splash):
        splash_dir = os.path.join(os.environ['HOME'], 'splash')
    else:
        print("PySPLASH ERROR: Could not locate SPLASH directory")
        print("Please make sure that you have SPLASH installed.")
        print("If you do not have admin privledges, please set an")
        print("environment variable `SPLASH_DIR` that points to the")
        print("directory where SPLASH is located.")
        exit(1)

    return splash_dir

splash_dir = get_splash_dir()

def build(splash_dir=splash_dir, compiler='gfortran', clean_first=False):
    libs = ['libexact', 'libread']

    print("\n>>> Building fortran source in directory: ", splash_dir, flush=True)

    errcode = 0

    if clean_first:
        errcode += subprocess.call(['make', 'clean'], cwd=splash_dir)

    for lib in libs:
        print("\nBuilding {}:".format(lib), flush=True)
        errcode += subprocess.call(['make','SYSTEM={}'.format(compiler),lib], cwd=splash_dir)
        print('\nCopying {}.so to pysplash/libs/. \n'.format(lib))
        errcode += subprocess.call(['cp', os.path.join(splash_dir,'build/{}.so'.format(lib)), os.path.join(src_dir, 'libs/.')])

    if errcode != 0:
        print('PySPLASH ERROR:')
        print('Could not build and copy library.')
        exit(1)

    print("<<< Finished building fortran source.\n", flush=True)


"""
Build the fortran library first, then do regular run()
"""
class custom_bdist_wheel(bdist_wheel):
    def run(self):
        build()
        bdist_wheel.run(self)

class custom_install(install):
    def run(self):
        # Don't recompile if bdist_wheels was already run
        if self._called_from_setup(inspect.currentframe()):
            build()
        install.run(self)

class custom_develop(develop):
    def run(self):
        # Don't recompile if uninstalling
        if not self.uninstall:
            build()
        develop.run(self)

print('\n>>>>> running setup.py >>>>>', flush=True)
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
    package_data=package_data,
    include_package_data=True,
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
    cmdclass={
        'install': custom_install,
        'bdist_wheel': custom_bdist_wheel,
        'develop': custom_develop,
    },
)
print('<<<<< end running setup.py <<<<<\n', flush=True)
