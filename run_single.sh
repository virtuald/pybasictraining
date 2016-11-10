#!/bin/bash

MAXTESTS=5

if [ "$1" == "" ]; then
    echo "Usage: ./run_single.sh TEST_NUMBER"
    exit 1
fi

TEST_PYTHONPATH=${TEST_PYTHONPATH:-../src}

TESTNAME=test_challenges.py::test_$1
shift

cd $(dirname $0)/tests/
PYTHONPATH="${TEST_PYTHONPATH}" python3 -m pytest -l "$@" $TESTNAME
