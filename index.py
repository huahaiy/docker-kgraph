#!/usr/bin/python
"""Index a CSV file for KNN search.  """

import sys, getopt 
import numpy as np
import pykgraph as kg

__author__ = "Huahai Yang"
__copyright__ = "Copyright 2015, Juji, Inc."
__license__ = "BSD"
__maintainer__ = "Huahai Yang"
__email__ = "hyang@juji-inc.com"
__status__ = "Development"

def main(argv):
    # A csv filename
    datafile = ''
    try:
        opts, args = getopt.getopt(argv, "hf:", ["datafile="])
    except getopt.GetoptError:
        print 'index.py -f <datafile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'index.py -f <datafile>'
            sys.exit()
        elif opt in ("-f", "--datafile"):
            datafile = arg

    data = np.genfromtxt(datafile, delimiter=',')
    (m, n) = data.shape

    pids = data[:, 0]
    scores = data[:, 1:n]

    # kgraph requires the number of columns to be multiple of 4 
    needed = 4 - (n - 1) % 4
    padded = np.zeros((m, n - 1 + needed))
    padded[:, :-needed] = scores

    index = kg.KGraph()
    index.build(padded)
    index.save(datafile + '.index')

if __name__ == "__main__":
    main(sys.argv[1:])
