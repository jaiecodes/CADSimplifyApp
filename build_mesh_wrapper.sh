#!/bin/bash
set -e

cd src/simplifyapp/resources
rm -rf build
mkdir build
cd build

cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_FIND_LIBRARY_SUFFIXES=.a \
  -DCMAKE_VERBOSE_MAKEFILE=ON
cmake --build . --config Release
mkdir -p ../bin
cp mesh_wrapper ../bin/
echo "Binary located at: src/simplifyapp/resources/bin/mesh_wrapper"
