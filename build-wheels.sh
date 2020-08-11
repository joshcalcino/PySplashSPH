#!/bin/bash -e

# If MANYLINUX is not set, assume no
if [ -z "$MANYLINUX" ]; then
  MANYLINUX=no
fi

#-- Make sure variables are not used uninitialised
set -u

# Use manylinux pythons if MANYLINUX=yes
# otherwise use default system python
if [ "${MANYLINUX}" == "yes" ]; then
  PYTHONS=/opt/python/cp3*/bin/python
else
  PYTHONS=python
fi

OS=$(uname -s)
ARCH=$(uname -m)

# Choose between delocate and auditwheel, and set the directory
# (within the package) to copy the external libraries to.
# Also, hardcode the platform tag for MacOS, otherwise deallocate won't work.
# Note that auditwheel will automatically change the platform tag for manylinux
# using the $AUDITWHEEL_PLAT environment variable.
if [ "${OS}" == "Darwin" ]; then
  DELOCATE_TOOL='delocate-wheel'
  DELOCATE_CMD='delocate-wheel -v'
  LIB_DIR=libs/.dylibs
  PLAT=macosx_10_9_x86_64
  PLAT_FLAG="--plat-name ${PLAT}"
else
  DELOCATE_TOOL='auditwheel'
  DELOCATE_CMD='auditwheel repair'
  LIB_DIR=/libs/

  # Set platform for standard linux
  # (auditwheel on manylinux images takes care of correct platform tag)
  if [ "${MANYLINUX}" == "yes" ]; then
    PLAT_FLAG=
  else
    PLAT="linux_${ARCH}"
    PLAT_FLAG="--plat-name ${PLAT}"
  fi
fi

if ! hash ${DELOCATE_TOOL} >/dev/null 2>&1; then
  echo "You need ${DELOCATE_TOOL} installed to use this script"
  exit 1
fi

# Set directories for bad and good wheels
BAD_WHEELS=.tmpwheelhouse
WHEELHOUSE=wheelhouse

# Clean out any old wheels in the bad wheels folder (if present)
rm ${BAD_WHEELS}/*.whl || true

# Compile wheels
for PYTHON in $PYTHONS; do
  # Clean build dir
  ${PYTHON} setup.py clean --all
  rm src/libs/*.so || true
  # Create wheel
  ${PYTHON} setup.py bdist_wheel ${PLAT_FLAG} --dist-dir ${BAD_WHEELS}
done

# Delocate wheels (remove external lib dependencies by including relevant libs in wheel)
# Note: these tools also relink libraries for you by modifying their ELFs
for whl in ${BAD_WHEELS}/*.whl; do
  ${DELOCATE_CMD} -L ${LIB_DIR} -w ${WHEELHOUSE} ${whl}
done

# Delete the bad wheels folder
rm -rf ${BAD_WHEELS} || true
