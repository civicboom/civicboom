#!/bin/bash
export PYTHONPATH=../lib
if [$1 = ""]
then
  nosetests
else
  echo "Civicboom Test: $1"
  nosetests civicboom/tests/functional/test_$1.py
fi
