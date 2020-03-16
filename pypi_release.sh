#!/bin/bash

echo "running test with tox..."
tox > tox_output.txt

if [[ $? -eq 0 ]]; then
    echo "clean up old builds..."
    rm -rf build
    rm -rf dist

    # build the dist and the wheel
    clear
    echo "build dist and wheel..."
    python setup.py sdist bdist_wheel

    # upload to pypi
    clear
    echo "upload to pypi..."
#    twine upload dist/*
else
    clear
    echo "TESTING WAS NOT SUCCESSFUL. Check tox_output.txt"
fi