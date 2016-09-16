# REFPROP-cmake
Small repo with CMake build system for building REFPROP shared library

Pre-Requisites
--------------

* Python
* A fortran compiler
* Cmake

Instructions
------------

1. Do a recursive(!) clone of this repository (e.g. ``git clone --recursive https://github.com/usnistgov/REFPROP-cmake.git``)
2. Copy the FORTRAN directory from your REFPROP installation into the root of your checked out code (or see below about using the path directly)
3. Open a console in the root of the cloned repository
4. ``mkdir build``
5. ``cd build``
6. ``cmake .. -DCMAKE_BUILD_TYPE=Release``
7. ``cmake --build .``

Once the shared library has been build, you will need to place it somewhere that your operating system knows where to find it.  On windows, that would be on the ``PATH`` environment variable.  On OSX, that would be one of the default shared library locations (see [apple docs](https://developer.apple.com/library/content/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/UsingDynamicLibraries.html) ).

OSX Notes
---------

* If you want to force a 32-bit build (I'm looking at you Excel 2016 on Mac), you can do:

    ``cmake .. -DREFPROP_32BIT=ON``

* On OSX, it seems you need to use the ``homebrew`` version of ``gcc`` and ``gfortran``, which you can do with a ``brew install gcc`` once homebrew is installed

Notes
-----

* Platforms other than windows (and sort of OSX) are CASE-SENSITIVE!  The folder ``fortran`` is not the same as ``FORTRAN``

* If you don't want to copy the FORTRAN directory to the root of the checked out code, you can alternatively pass the cmake flag ``REFPROP_FORTRAN_PATH`` as in something like:
    
    ``cmake .. -DREFPROP_FORTRAN_PATH=/path/to/refprop/fortran``

  If the path has spaces in it, you need to quote-escape the path

* On windows, if you want to use Intel Fortran + Visual Studio, you can change the generator, with something like:

    ``cmake .. -G "Visual Studio 11 2012 Win64"``

  Run ``cmake --help`` to see a complete list of supported generators (not all of which will support FORTRAN)

  When building with a Visual Studio generator, you will want to ensure that you get a Release build, which is ensured by passing the flag ``--config Release`` to the build command, something like:

    ``cmake --build . --config Release``