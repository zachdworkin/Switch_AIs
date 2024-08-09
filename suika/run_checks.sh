#!/bin/bash

source ./bootstrap.sh
echo "Running black"
black --check --diff ./suika
echo "Running pylint"
pylint -d duplicate-code -d fixme ./suika
echo "Running mypy"
mypy suika --check-untyped-defs --disallow-untyped-decorators

exit 0
