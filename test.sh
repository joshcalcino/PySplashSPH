#!/bin/bash -e

# If MANYLINUX is not set, assume no
if [ -z "$MANYLINUX" ]; then
  MANYLINUX=no
fi

err=0

if [ "${MANYLINUX}" == "yes" ]; then

  # Check that AUDITWHEEL is set
  if [ -z "$AUDITWHEEL_PLAT" ]; then
    echo "This doesn't look like a manylinux image. AUDITWHEEL_PLAT is not set!"
    exit 1
  fi

  #-- Don't allow uninitialised variables; don't exit on error
  set -u +e

  PYBINS=/opt/python/cp35*/bin
  for PYBIN in $PYBINS; do
    # Install wheel
    ${PYBIN}/pip install wheelhouse/pysplash*py3*${AUDITWHEEL_PLAT}.whl; err=$((err+$?))
    # Run test
    ${PYBIN}/python test/test_read.py; err=$((err+$?))
  done
  set -e

else
  # Don't allow uninitialised variables
  set -u

  OS=$(uname -s)
  ARCH=$(uname -m)

  if [ "${OS}" == "Darwin" ]; then
    PLAT=macosx_10_9_x86_64
  else
    PLAT=linux_${ARCH}
  fi

  # Check that virtual env is installed
  if ! hash virtualenv >/dev/null 2>&1; then
    echo "You need virtualenv installed to use this script"
    exit 1
  fi

  # Clean any existing test venv
  rm -rf ./test/venv || true

  # Create a virtual env and activate it
  virtualenv ./test/venv
  source test/venv/bin/activate

  # Don't exit on error
  set +e

  # Install the wheel in the virtual env
  pip install wheelhouse/pysplash*py3*${PLAT}.whl; err=$((err+$?))

  # Run tests
  python test/test_read.py; err=$((err+$?))

  # Exit on error
  set -e

  # Remove test venv
  rm -rf ./test/venv || true

fi

if ! [ "$err" == "0" ]; then
  echo "FAIL: $err test(s) failed!"
  exit 1
else
  echo "PASS"
fi
