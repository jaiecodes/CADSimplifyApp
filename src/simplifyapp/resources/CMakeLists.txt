cmake_minimum_required(VERSION 3.12)
project(mesh_wrapper)

# Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Prefer static libraries over dynamic (.a instead of .dylib)
set(CMAKE_FIND_LIBRARY_SUFFIXES .a ${CMAKE_FIND_LIBRARY_SUFFIXES})

# Ensure Release build for optimizations
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# Find CGAL
find_package(CGAL REQUIRED)

# Create executable
add_executable(mesh_wrapper mesh_wrapper.cpp)

# Link CGAL (header-only for most use, but this ensures 3rd party deps like GMP/MPFR are linked)
target_link_libraries(mesh_wrapper CGAL::CGAL)

# Optional: Strip unused symbols in Release mode
if(CMAKE_BUILD_TYPE STREQUAL "Release")
  if (APPLE)
    target_link_options(mesh_wrapper PRIVATE -Wl,-dead_strip)
  elseif(UNIX)
    target_link_options(mesh_wrapper PRIVATE -Wl,--strip-all)
  endif()
endif()
