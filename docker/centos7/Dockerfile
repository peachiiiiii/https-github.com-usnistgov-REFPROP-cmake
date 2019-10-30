FROM centos:7


RUN yum -y update && \
    yum -y install  wget ssh make gcc gcc-c++ gcc-gfortran cmake git nano python3 python3-pip && \
    yum -y clean all

# This ADD block forces a build (invalidates the cache) if the git repo contents have changed, otherwise leaves it untouched.
ADD https://api.github.com/repos/usnistgov/REFPROP-cmake/git/refs/heads/master RPcmake-version.json
RUN git clone --recursive https://github.com/usnistgov/REFPROP-cmake && \
    cd REFPROP-cmake/ && \
    mkdir build && \
    cd build/

# Soft-link pip3->pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# start by registering python2 as an alternative
# register python3.5 as an alternative
# Give python3 precedence when you type python
RUN alternatives --install /usr/bin/python python /usr/bin/python2 50 && \
    alternatives --install /usr/bin/python python /usr/bin/python3.6 60

# Install numpy from pip
RUN pip install numpy six && python -c "import numpy; print(numpy.__version__)"
