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

Notes
-----

* Platforms other than windows (and sort of OSX) are CASE-SENSITIVE!  The folder ``fortran`` is not the same as ``FORTRAN``

* If you don't want to copy the FORTRAN directory to the root of the checked out code, you can alternatively pass the cmake flag ``REFPROP_FORTRAN_PATH`` as in something like:
    
      cmake .. -DREFPROP_FORTRAN_PATH=/path/to/refprop/fortran

  If the path has spaces in it, you need to quote-escape the path

* On windows, if you want to use Intel Fortran + Visual Studio, you can change the generator, with something like:

      cmake .. -G "Visual Studio 11 2012 Win64"

  Run ``cmake --help`` to see a complete list of supported generators (not all of which will support FORTRAN)

  When building with a Visual Studio generator, you will want to ensure that you get a Release build, which is ensured by passing the flag ``--config Release`` to the build command, something like:

      cmake --build . --config Release