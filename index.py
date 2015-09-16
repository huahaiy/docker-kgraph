import sys, getopt
from numpy import genfromtxt

data = genfromtxt('fashion-style-data.csv', delimiter=',')
(m, n) = data.shape
pids = data[:,0]
scores = data[:,1:n]
