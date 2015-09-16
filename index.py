import sys, getopt
import numpy as np

data = np.genfromtxt('fashion-style-data.csv', delimiter=',')
(m, n) = data.shape
pids = data[:,0]
scores = data[:,1:n]
