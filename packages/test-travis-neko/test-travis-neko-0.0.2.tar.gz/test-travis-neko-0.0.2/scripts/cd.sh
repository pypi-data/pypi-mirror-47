#!/bin/sh

if [[ -z "${PYPI_USERNAME}" ]]; then echo "Missing PYPI_USERNAME environment variable" >&2; exit 1; fi
if [[ -z "${PYPI_PASSWORD}" ]]; then echo "Missing PYPI_PASSWORD environment variable" >&2; exit 1; fi

set -o errexit

python setup.py bdist_wheel
twine upload dist/* -u "${PYPI_USERNAME}" -p "${PYPI_PASSWORD}"
