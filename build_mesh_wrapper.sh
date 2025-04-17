#!/bin/bash
set -e

echo "🔄 Cleaning previous build..."
cd src/simplifyapp/resources
rm -rf build
mkdir build
cd build

echo "🔧 Configuring build with CMake..."
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_FIND_LIBRARY_SUFFIXES=.a \
  -DCMAKE_VERBOSE_MAKEFILE=ON

echo "🔨 Building mesh_wrapper..."
cmake --build . --config Release

echo "🚚 Copying binary to ../bin/"
mkdir -p ../bin
cp mesh_wrapper ../bin/

echo "✅ Done! Binary located at: src/simplifyapp/resources/bin/mesh_wrapper"
