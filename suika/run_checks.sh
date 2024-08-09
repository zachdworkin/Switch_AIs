#!/bin/bash

source ./bootstrap.sh
black --check ./suika
pylint -d duplicate-code -d fixme ./suika
mypy suika --check-untyped-defs --disallow-untyped-decorators

exit 0
