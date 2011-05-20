#!/bin/bash
export PYTHONPATH=../lib
echo "Civicboom Test: $1"
nosetests civicboom/tests/functional/test_$1.py

