"""PySplashSPH setup.py."""

import io
import pathlib
import inspect
import subprocess

from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from wheel.bdist_wheel import bdist_wheel
from os import environ
from os.path import join, basename, isfile, abspath

splash_error = """
pysplashsph ERROR: Could not locate SPLASH directory
Please make sure that you have SPLASH installed in one of the following directories.

1. In the current directory, i.e. ./splash/
2. In the parent directory, i.e. ../splash/
3. In $SPLASH_DIR
4. In $HOME/splash

Note: you may have to do `git submodule update` if you're using the first option.
"""

def get_splash_dir():
    """
    Locate splash installation.

    Locations are checked in this order:
    1) Parent directory
    2) Environment variable $SPLASH_DIR
    3) $HOME/splash
    """
    current_dir = str(pathlib.Path(abspath(__file__)).parent)
    parent_dir  = str(pathlib.Path(current_dir).parent)
    home_splash = join(environ['HOME'], 'splash')
    cwd_splash  = join(current_dir, 'splash')

    if isfile(join(cwd_splash, 'Makefile')):
        splash_dir = cwd_splash
    elif 'splash' == basename(parent_dir) and isfile(join(parent_dir, 'Makefile')):
        splash_dir = parent_dir
    elif 'SPLASH_DIR' in environ and isfile(join(environ['SPLASH_DIR'], 'Makefile')):
        splash_dir = environ['SPLASH_DIR']
    elif isfile(join(home_splash, 'Makefile')):
        splash_dir = home_splash
    else:
        print(splash_error)
        exit(1)

    return splash_dir

splash_dir = get_splash_dir()

def build(splash_dir=splash_dir, compiler='gfortran', clean_first=False):
    libs = ['libexact', 'libread']

    print("\n>>> Building fortran source in directory: ", splash_dir, flush=True)

    errcode = 0

    if clean_first:
        errcode = subprocess.call(['make', 'clean'], cwd=splash_dir)
        if errcode != 0:
            print('pysplashsph ERROR:')
            print('Could not "make clean"')
            exit(1)

    for lib in libs:
        print("\nBuilding {}:".format(lib), flush=True)
        errcode = subprocess.call(['make','SYSTEM={}'.format(compiler),lib], cwd=splash_dir)
        if errcode != 0:
            print('pysplashsph ERROR:')
            print('Could not build library.')
            exit(1)

        print('\nCopying {}.so to pysplashsph/libs/. \n'.format(lib), flush=True)
        errcode = subprocess.call(['cp', join(splash_dir,'build/{}.so'.format(lib)), join('pysplashsph', 'libs/.')])
        if errcode != 0:
            print('pysplashsph ERROR:')
            print('Could not copy library.')
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
    package_data={"pysplashsph": ["libs/*.so*", "libs/*.dylib*"]},
    cmdclass={
        'install': custom_install,
        'bdist_wheel': custom_bdist_wheel,
        'develop': custom_develop,
    },
)
print('<<<<< end running setup.py <<<<<\n', flush=True)
