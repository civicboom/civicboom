#!/bin/bash

cd `dirname $0`

export PYTHONPATH=../lib
make ini

if [ x$1 = x ]
then
  nosetests
else
  echo "Civicboom Test: $1"
  nosetests civicboom/tests/functional/test_$1.py
fi
