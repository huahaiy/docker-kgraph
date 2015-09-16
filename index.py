#!/usr/bin/python

import sys 
import getopt as opt
import numpy as np
import pykgraph as kg

def main(argv):
    # A csv filename
    datafile = ''
    try:
        opts, args = opt.getopt(argv, "hf", ["datafile="])
    except opt.GetoptError:
        print 'index.py -f <datafile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'index.py -f <datafile>'
            sys.exit()
        elif opt in ("-f", "--file"):
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
