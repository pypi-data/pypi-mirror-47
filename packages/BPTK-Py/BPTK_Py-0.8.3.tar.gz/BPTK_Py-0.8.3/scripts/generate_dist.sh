#!/bin/sh
cd ..
rm -rf BPTK_Py/sd-compiler/node_modules/
rm -rf build/
rm -rf dist/
python3 setup.py sdist bdist_wheel

