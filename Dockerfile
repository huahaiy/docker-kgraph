#
# Run kgraph KNN search service on HTTP 
#
# Version     0.1
#
FROM huahaiy/debian

MAINTAINER Huahai Yang <hyang@juji-inc.com>

RUN \
  echo "===> install dependencies..."  && \ 
  apt-get update  && \
  apt-get install -y --force-yes git ssh-client libboost-all-dev python-numpy libopenblas-dev  && \
  \
  \
  echo "===> build "  && \
  git clone git@github.com:aaalgo/kgraph.git && \
  cd kgraph && \
  make install
  \
  \
  echo "===> clean up..."  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

