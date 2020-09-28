#!/bin/bash -eu

if ! hash twine >/dev/null 2>&1; then
  echo "You need twine installed to use this script"
  exit 1
fi

twine upload              \
  --skip-existing         \
  -u "${TWINE_USERNAME}"  \
  -p "${TWINE_PASSWORD}"  \
  wheelhouse/*
