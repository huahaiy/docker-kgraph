# docker-kgraph

Run KGraph K nearst neighbor search service over HTTP. 

Currently only indexing and searching of one CSV data file is supported. The first column of the data file should be some kind of IDs of the rows to be indexed. The rest of the columns should all be float numbers. The CSV file should NOT have a header line. The columns should be identified positionally.

## index

First put the data file in the volume accessible to the container. Then run index.py like this: 

  docker run  -v your.data.csv:/kgraph/your.data.csv \
              -it huahaiy/kgraph  \
              index.py -f /kgraph/your.data.csv

Check that an index file called your.data.csv.index is created in the same location.

## search

search.py is running as a simple HTTP service on default port 8071. "-p port" allows one to change the port, but make sure expose that port too, like so:

  docker run  -v your.data.csv:/kgraph/your.data.csv \
              -p 8080:8080
              -it huahaiy/kgraph  \
              search.py -p 8080 -f /kgraph/your.data.csv

The search URL is something like this: 
  http://localhost:8080/search?k=10&q=0.2,0,3,0.3

Here we ask for 10 nearst neighors of the vector [0.2, 0.3, 0.3]. Make sure the length of the query vector is the same as your data file column numbers (minus one for the IDs column).

If all goes well, the JSON response will be something like this 
  {'ids': [id1, id2, id3, ..., id10], 
   'dists': [0.003, 0.004, 0.007, ..., 0.012]}

So we return both the IDs of the nearest neighbors and the corresponding distances to the query vector.
