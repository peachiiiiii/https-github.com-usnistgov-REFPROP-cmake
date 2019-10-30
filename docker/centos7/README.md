Once you have docker installed, and you can do something like
```
docker run hello-world
```

Copy the FORTRAN files for REFPROP into folder ``RP10src`` in this folder

In this folder, build the image
```
docker built -t rpco7 .
```

Bash into the container
```
docker run -it -v"$(CWD)":/shared  -t rpco7 bash
```

Then inside the container:
```
cd /REFPROP-cmake/build
cmake -DREFPROP_FORTRAN_PATH=/shared/RP10src
cmake --build .
```

Should yield something like
```
$ docker run -it -v"${PWD}":/shared -t rpco7 bash
[root@7221984c6cb1 /]# cd REFPROP-cmake/build
[root@7221984c6cb1 build]# cmake .. -DREFPROP_FORTRAN_PATH=/shared/RP10src/
-- The C compiler identification is GNU 4.8.5
-- The CXX compiler identification is GNU 4.8.5
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- The Fortran compiler identification is GNU
-- Check for working Fortran compiler: /usr/bin/gfortran
-- Check for working Fortran compiler: /usr/bin/gfortran  -- works
-- Detecting Fortran compiler ABI info
-- Detecting Fortran compiler ABI info - done
-- Checking whether /usr/bin/gfortran supports Fortran 90
-- Checking whether /usr/bin/gfortran supports Fortran 90 -- yes
-- Found PythonInterp: /usr/bin/python (found version "3.6.8") 
-- DEFSYM_FLAG: --using-defsym
-- linux
Missing from PASS_CMN_tokens:  []
Missing from REFPROP_lib.h: ['FNCRPTdll', 'VIRTAUdll']

-- Configuring done
-- Generating done
-- Build files have been written to: /REFPROP-cmake/build
[root@7221984c6cb1 build]# cmake --build .
Scanning dependencies of target REFPROP_H
[  6%] About to build the REFPROP.h header file w/ /usr/bin/python;-u;/REFPROP-cmake/externals/REFPROP-headers/generate_header.py;--FORTRAN-path;/shared/RP10src/;--python-exe;/usr/bin/python
Writing the .pyf file with numpy.f2py, please be patient...
Deleting REFPROP.pyf
[  6%] Built target REFPROP_H
Scanning dependencies of target refprop
[ 13%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/CORE_PR.FOR.o
[ 20%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/SETUP.FOR.o
[ 26%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/TRNSP.FOR.o
[ 33%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/REFPROP.FOR.o
/shared/RP10src/REFPROP.FOR:5684.72:

         if (ABS(iErrPrnt).eq.3) pause           !If your compiler compl
                                                                        1
Warning: Deleted feature: PAUSE statement at (1)
[ 40%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/PROP_SUB.FOR.o
[ 46%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/TRNS_VIS.FOR.o
[ 53%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/TRNS_TCX.FOR.o
[ 60%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/CORE_ANC.FOR.o
[ 66%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/CORE_FEQ.FOR.o
[ 73%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/MIX_HMX.FOR.o
[ 80%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/SAT_SUB.FOR.o
[ 86%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/FLSH_SUB.FOR.o
[ 93%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/UTILITY.FOR.o
[100%] Building Fortran object CMakeFiles/refprop.dir/shared/RP10src/PASS_FTN.FOR.o
Linking Fortran shared library librefprop.so
[100%] Built target refprop
```
