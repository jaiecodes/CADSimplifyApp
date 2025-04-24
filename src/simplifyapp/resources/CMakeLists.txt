cmake_minimum_required(VERSION 3.12)
project(mesh_wrapper)

# C++17 is required for CGAL
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optional: Prefer static libraries
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_FIND_LIBRARY_SUFFIXES .a ${CMAKE_FIND_LIBRARY_SUFFIXES})

# Use vcpkg toolchain if provided
if(DEFINED CMAKE_TOOLCHAIN_FILE)
  message(STATUS "Using vcpkg toolchain: ${CMAKE_TOOLCHAIN_FILE}")
endif()

# Ensure Release build
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# Find CGAL and dependencies
find_package(CGAL REQUIRED)
find_package(Boost REQUIRED)
find_package(GMP REQUIRED)
find_package(MPFR REQUIRED)

# Executable
add_executable(mesh_wrapper mesh_wrapper.cpp)

# Link everything statically
target_link_libraries(mesh_wrapper
  CGAL::CGAL
  ${Boost_LIBRARIES}
  ${GMP_LIBRARIES}
  ${MPFR_LIBRARIES}
)

# Optional: Strip unused symbols in Release mode
if(CMAKE_BUILD_TYPE STREQUAL "Release")
  if(WIN32)
    target_link_options(mesh_wrapper PRIVATE /DEBUG:NONE /INCREMENTAL:NO /OPT:REF /OPT:ICF)
  elseif(APPLE)
    target_link_options(mesh_wrapper PRIVATE -Wl,-dead_strip)
  elseif(UNIX)
    target_link_options(mesh_wrapper PRIVATE -Wl,--strip-all)
  endif()
endif()