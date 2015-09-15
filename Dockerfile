#
# Run kgraph KNN search service on HTTP 
#
# Version     0.1
#
FROM huahaiy/debian

MAINTAINER Huahai Yang <hyang@juji-inc.com>

ADD kgraph /kgraph

RUN \
  echo "===> install dependencies..."  && \ 
  apt-get update  && \
  apt-get install -y --force-yes build-essential git libboost-timer-dev \
    libboost-chrono-dev libboost-program-options-dev libboost-system-dev \
    libboost-python-dev python-numpy libopenblas-dev  

RUN \
  echo "===> build "  && \
  cd /kgraph && \
  sed -i 's/libblas/libopenblas/' /kgraph/python/Makefile && \
  make && \
  make install && \
  make clean && \
  \
  \
  echo "===> clean up..."  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

