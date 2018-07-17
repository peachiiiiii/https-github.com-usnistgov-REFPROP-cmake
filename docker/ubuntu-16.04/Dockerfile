FROM ubuntu:16.04

RUN apt-get -y -m update && \
    apt-get install -y git cmake g++ gfortran python python-numpy python-pip python-six

RUN git clone --recursive https://github.com/usnistgov/REFPROP-cmake && \
    cd REFPROP-cmake/ && \
    mkdir build && \
    cd build/ && \
    cmake .. -DREFPROP_FORTRAN_PATH=/91/FORTRAN && \
    cmake --build .