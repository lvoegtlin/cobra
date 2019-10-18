#!/bin/bash

echo "clean up old builds..."
rm -rf build
rm -rf dist

# build the dist and the wheel
echo "build dist and wheel..."
python setup.py sdist bdist_wheel

# upload to pypi
echo "upload to pypi..."
twine upload dist/*