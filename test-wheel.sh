#!/bin/bash -e

# If MANYLINUX is not set, assume no
if [ -z "$MANYLINUX" ]; then
  MANYLINUX=no
fi

err=0

if [ "${MANYLINUX}" == "yes" ]; then

  # Check that AUDITWHEEL is defined
  if [ -z "$AUDITWHEEL_PLAT" ]; then
    echo "This doesn't look like a manylinux image. AUDITWHEEL_PLAT is not defined"
    exit 1
  fi
  #-- Don't allow uninitialised variables
  set -u

  yum -y install hdf5-devel
  WHEEL=wheelhouse/pysplashsph*py3*${AUDITWHEEL_PLAT}.whl
  PYBINS=/opt/python/cp3[6-8]*/bin

  # Install the wheel, run tests
  # and catch error codes
  # (without stopping if errors)
  set +e
  for PYBIN in $PYBINS; do
    echo "--- Updating pip ---"
    ${PYBIN}/python -m pip install --upgrade pip
    echo "--- Testing with ${PYBIN} ---"
    echo "Installing wheel"
    ${PYBIN}/pip install ${WHEEL} pytest
    ${PYBIN}/pytest -s; err=$((err+$?))
  done
  set -e

else

  # Check that virtualenv is installed
  for ITEM in virtualenv; do
    if ! hash ${ITEM} >/dev/null 2>&1; then
      echo "You need ${ITEM} installed to use this script"
      exit 1
    fi
  done
  # Don't allow uninitialised variables
  set -u

  # Detect platform
  OS=$(uname -s)
  ARCH=$(uname -m)
  if [ "${OS}" == "Darwin" ]; then
    PLAT=macosx_10_9_x86_64
  else
    PLAT=linux_${ARCH}
  fi
  WHEEL=wheelhouse/pysplashsph*py3*${PLAT}.whl

  # Clean any existing test venv
  rm -rf ./test/venv || true

  echo "Creating virtual env for testing"
  virtualenv ./test/venv
  source test/venv/bin/activate

  # Install the wheel in the virtual env,
  # run tests and catch error codes
  # (without stopping if errors)
  set +e
  echo "Testing wheel"
  pip install ${WHEEL} pytest
  pytest -s; err=$((err+$?))
  set -e

  echo "Deleting virtual env"
  rm -rf ./test/venv || true

fi

if ! [ "$err" == "0" ]; then
  echo "FAIL"
else
  echo "PASS"
fi

exit $err
