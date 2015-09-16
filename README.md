# docker-kgraph

Run KGraph K nearst neighbor search service over HTTP. 

Currently only indexing and searching of one CSV data file is supported. The first column of the data file should be some kind of IDs of the rows to be indexed. The rest of the columns should all be float numbers. The CSV file should NOT have a header line. The columns should be identified positionally.

## index

Put your data file in a local directory that will be linked to the container volume /kgraph, and run indexer like this: 

    docker run  -v <local_directory>:/kgraph \
                -t huahaiy/kgraph  \
                index.py -f /kgraph/<your.file>

After finsing the indexing, check that a file called `<your.file>.index` is created in the same directory.

## search

Search is running as a simple HTTP service on default port 8071. `-p` option allows one to change the port. Make sure to expose that port from container, like so:

    docker run  -v <local_directory>:/kgraph \
                -p 8080:8080
                -it huahaiy/kgraph  \
                search.py -p 8080 -f /kgraph/<your.file>

The search URL is something like this: 

    http://localhost:8080/search?k=10&q=0.2,0,3,0.3

Here we ask for 10 nearst neighors of the vector [0.2, 0.3, 0.3]. Make sure the length of the query vector is the same as your data file column numbers (minus one for the IDs column).

If all goes well, the JSON response will be something like this 

    {'ids': [id1, id2, id3, ..., id10], 
     'dists': [0.003, 0.004, 0.007, ..., 0.012]}

So we return both the IDs of the nearest neighbors and the corresponding distances to the query vector.
