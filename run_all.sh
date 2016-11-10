#!/bin/bash

TEST_PYTHONPATH=${TEST_PYTHONPATH:-../src}

cd $(dirname $0)/tests/
PYTHONPATH="${TEST_PYTHONPATH}" python3 -m pytest -l "$@"
