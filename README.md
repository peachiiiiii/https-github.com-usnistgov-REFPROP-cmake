# REFPROP-cmake

Small repo with CMake build system for building REFPROP shared library

Why you should use this build system:

* The windows-style mixed-case symbols are export on all platforms (for instance there is **ALWAYS** a ``SETUPdll`` symbol, which means you can write a clean cross-platform interface).  This magic is achieved with export aliases.
* You can easily point the repo at a different version of the REFPROP sources, allowing for building/testing several versions of REFPROP in parallel

Brought to you by Ian Bell, NIST, ian.bell@nist.gov

## License

Public domain, (though REFPROP itself is not public domain)

## Pre-Requisites

* Python + numpy
* A fortran compiler
* Cmake
* git

## Instructions

1. Do a recursive(!) clone of this repository (e.g. ``git clone --recursive https://github.com/usnistgov/REFPROP-cmake.git``)
2. Copy the FORTRAN directory from your REFPROP installation into the root of your checked out code (or see below about using the path directly)
3. Open a console in the root of the cloned repository
4. ``mkdir build``
5. ``cd build``
6. ``cmake .. -DCMAKE_BUILD_TYPE=Release``
7. ``cmake --build .``

Once the shared library has been build, you will need to place it somewhere that your operating system knows where to find it.  On windows, that would be on the ``PATH`` environment variable.  On OSX, that would be one of the default shared library locations (see [apple docs](https://developer.apple.com/library/content/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/UsingDynamicLibraries.html) ).

## OSX Notes

* If you want to force a 32-bit build (I'm looking at you Excel 2016 on Mac), you can do:

    ``cmake .. -DREFPROP_32BIT=ON``

* On OSX, it seems you need to use the ``homebrew`` version of ``gcc`` and ``gfortran``.  You can obtain homebrew versions of gcc and gfortran with ``brew install gcc`` once homebrew is installed

## General Notes

* Platforms other than windows (and sort of OSX) are CASE-SENSITIVE!  The folder ``fortran`` is not the same as ``FORTRAN``

* If you don't want to copy the FORTRAN directory to the root of the checked out code, you can alternatively pass the cmake flag ``REFPROP_FORTRAN_PATH`` as in something like:
    
    ``cmake .. -DREFPROP_FORTRAN_PATH=/path/to/refprop/fortran``

  If the path has spaces in it, you need to quote-escape the path

* On windows, if you want to use Intel Fortran + Visual Studio, you can change the generator, with something like:

    ``cmake .. -G "Visual Studio 11 2012 Win64"``

  Run ``cmake --help`` to see a complete list of supported generators (not all of which will support FORTRAN)

  When building with a Visual Studio generator, you will want to ensure that you get a Release build, which is ensured by passing the flag ``--config Release`` to the build command, something like:

    ``cmake --build . --config Release``

## Instructions for MINGW builds on windows

It is possible to use a fully open-source build system on windows to compile REFPROP.  This is enabled by the use of the MINGW compiler system.

To get started from a clean windows installation, you will need:
* [cmake](https://cmake.org/download/)
* [MINGW](https://sourceforge.net/projects/mingw-w64/files/latest/download) (make sure to install the gfortran compiler)
* [miniconda](https://conda.io/miniconda.html):  This installs a minimal python setup, along with with the ``conda`` package manager (use the 64-bit python 3.6 one). Once it is installed, install numpy with : ``conda install numpy`` at the command line
* [git](https://git-scm.com/download/win)

Then to set up your shell, at the command prompt do:
```
set PATH=D:\Software\mingw\bin;%PATH%
```
or put the path to wherever the MINGW compiler has been installed.

Check out the git sources with:
```
git clone --recursive https://github.com/usnistgov/REFPROP-cmake
```
Move into that directory:
```
cd REFPROP-cmake
```
Make a working directory
```
mkdir build
```
Move into that directory
```
cd build
```
Configure the build system
```
cmake .. -DREFPROP_FORTRAN_PATH=R:/FORTRAN -G "MinGW Makefiles" -DREFPROP_64BIT=ON -DCMAKE_BUILD_TYPE=Release
```
and build the DLL
```
cmake --build .
```
That's it!

or all in a tidy batch file that clones the repo, does the build, and cleans up after itself:

```
set PATH=D:\Software\mingw-w64\x86_64-7.2.0-posix-seh-rt_v5-rev0\mingw64\bin;%PATH%
git clone --recursive https://github.com/usnistgov/REFPROP-cmake
cd REFPROP-cmake
mkdir build
cd build
cmake .. -DREFPROP_FORTRAN_PATH=R:/FORTRAN -G "MinGW Makefiles" -DREFPROP_64BIT=ON -DCMAKE_BUILD_TYPE=Release
cmake --build .
cd ../..
copy REFPROP-cmake\build\REFPRP64.DLL .
rmdir /Q /S REFPROP-cmake
```