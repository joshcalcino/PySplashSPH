#!/bin/bash
set -e -u -x

if ! hash docker >/dev/null 2>&1; then
  echo "You need docker installed to use this script"
  exit 1
fi

# Assuming splash is in a subdirectory
SPLASH=./splash

# Launch a docker container and run build script in each manylinux image
for V in 1 2010 2014; do
  for ARCH in i686 x86_64; do
    PLAT="manylinux${V}_${ARCH}"
    DOCKER_IMAGE="quay.io/pypa/${PLAT}"
    cd ${SPLASH}; make clean; cd -
    docker run --rm -e MANYLINUX=yes -v `pwd`:/io/pysplashsph -w /io/pysplashsph $DOCKER_IMAGE ./build-wheels.sh
  done
done
