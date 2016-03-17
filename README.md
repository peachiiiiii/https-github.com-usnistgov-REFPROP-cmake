# REFPROP-cmake
Small repo with CMake build system for building REFPROP shared library

Pre-Requisites
--------------

* Python
* A fortran compiler
* Cmake

Instructions
------------

1. Do a recursive(!) clone of this repository (e.g. git clone --recursive https://github.com/usnistgov/REFPROP-cmake.git)
2. Copy the FORTRAN directory from your REFPROP installation into the root of your checked out code
3. mkdir build
4. cd build
5. cmake ..
6. cmake --build .

