FROM ubuntu:18.04

RUN apt-get -y -m update && \
    apt-get install -y git cmake g++ gfortran python3 python3-pip

# This ADD block forces a build (invalidates the cache) if the git repo contents have changed, otherwise leaves it untouched.
ADD https://api.github.com/repos/usnistgov/REFPROP-cmake/git/refs/heads/master RPcmake-version.json
RUN git clone --recursive https://github.com/usnistgov/REFPROP-cmake && \
    cd REFPROP-cmake/ && \
    mkdir build && \
    cd build/

# Soft-link pip3->pip and same for python
RUN ln -s /usr/bin/pip3 /usr/bin/pip && \
    ln -s /usr/bin/python3 /usr/bin/python

# Install numpy from pip
RUN pip install numpy && python -c "import numpy; print(numpy.__version__)"

