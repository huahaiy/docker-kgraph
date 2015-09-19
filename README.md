# docker-kgraph

This image contains some python code to run [KGraph](https://github.com/aaalgo/kgraph) K nearest neighbour search over a simple HTTP server. 

The input data should be in the format of comma separated CSV files. The first column of the data file should be some kind of IDs of the rows to be indexed. The rest of the columns should all be floating point numbers. The CSV data file should NOT have a header line. The data files must be indexed before becoming available for search. 

## index

Put your data file in a local directory that will be linked to the container volume /kgraph, and run indexer like this: 

    docker run  -v <local_directory>:/kgraph \
                -t huahaiy/kgraph  \
                index.py -f /kgraph/<data.file>


After indexing, check that a file called `<data.file>.index` is created in the same directory.

## search

Search is running as a simple HTTP service on default port 8071. `-p` option allows one to change the port. Make sure to expose that port from container, like so:

    docker run  -v <local_directory>:/kgraph \
                -p 8080:8080 \
                -it huahaiy/kgraph  \
                search.py -p 8080 \
                          -d <data.name1>,<data.name2>,<data.name3>
                          -f <data.file1>,<data.file2>,<data.file3>


As can be seen, multiple data sources can be specified for the searcher. `-d` gives the coma separated names assigned to each data files, which should correspond to the `d=` parameters in the search URL; `-f` are the corresponding data file names that were used during indexing. 

The search URL is something like this: 

    http://localhost:8080/search?d=data.name1&k=10&q=0.2,0,3,0.3


Here we ask for 10 nearest neighbours of the vector [0.2, 0.3, 0.3] in data.name1. Make sure the length of the query vector equals to the data file column numbers minus one (for the IDs column).

If all goes well, the JSON response will be something like this 

    {'ids': [id1, id2, id3, ..., id10], 
     'dists': [0.003, 0.004, 0.007, ..., 0.012]}


Here we return both the IDs of the nearest neighbours and the corresponding distances to the query vector. Currently, only Euclidean distances are supported.

## license

BSD, see LICENSE file
