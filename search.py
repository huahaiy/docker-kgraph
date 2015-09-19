#!/usr/bin/python
"""Provide KNN search service over HTTP.  """

import sys, getopt 
import json
import numpy as np
import pykgraph as kg

from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.routing import url
from wheezy.web.handlers import BaseHandler
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory

__author__ = "Huahai Yang"
__copyright__ = "Copyright 2015, Juji, Inc."
__license__ = "BSD"
__maintainer__ = "Huahai Yang"
__email__ = "hyang@juji-inc.com"
__status__ = "Development"


class SearchHandler(BaseHandler):

    def get(self):
	# TODO: check the params exist and validate them
        d = self.request.query.get('d')[0]
	k = int(self.request.query.get('k')[0])
	q = [[float(x) for x in self.request.query.get('q')]]

        dd = indices[d]
        n = dd['n']
        needed = dd['needed']
        index = dd['index']
        padded = dd['padded']
        pids = dd['pids']

    	pq = np.zeros((1, n - 1 + needed))
	pq[:, :-needed] = q

	result = index.search(padded, pq, K = k, withDistance = True)
	ids = map(lambda x: pids[x], result[0][0].tolist())

        return self.json_response({'ids': ids, 'dists': result[1][0].tolist()})


def welcome(request):
    response = HTTPResponse()
    response.write('Server is up!')
    return response


all_urls = [
    url('', welcome, name='default'),
    url('search', SearchHandler, name='search')
]


options = {}
web = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        path_routing_middleware_factory
    ],
    options=options
)


indices = {}

def load(entry, datafile):
    data = np.genfromtxt(datafile, delimiter=',')
    (m, n) = data.shape

    pids = data[:, 0]
    scores = data[:, 1:n]

    # kgraph requires the number of columns to be multiple of 4 
    needed = 4 - (n - 1) % 4
    padded = np.zeros((m, n - 1 + needed))
    padded[:, :-needed] = scores

    index = kg.KGraph()
    index.load(datafile + ".index")

    entry['m'] = m
    entry['n'] = n
    entry['pids'] = pids
    entry['needed'] = needed
    entry['padded'] = padded
    entry['index'] = index


def init(datanames, datafiles):
    names = datanames.split(',')
    files = datafiles.split(',')
	
    for i in range(0, len(names)):
	n = names[i]
        indices[n] = {} 
        load(indices[n], files[i]) 
	

def main(argv):
    datafiles = ''
    datanames = ''
    port = 8071
    try:
        opts, args = getopt.getopt(argv, "hp:f:d:", 
                ["port=", "datafiles=", "datanames="])
    except getopt.GetoptError:
        print 'search.py -p <port> -d <datanames> -f <datafiles>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'search.py -p <port> -d <datanames> -f <datafiles>'
            sys.exit()
        elif opt in ("-d", "--datanames"):
            datanames = arg
        elif opt in ("-f", "--datafiles"):
            datafiles = arg
	elif opt in ("-p", "--port"):
	    port = arg

    init(datanames, datafiles)

    from wsgiref.simple_server import make_server
    try:
        print('Server started on port ' + str(port))
        make_server('', port, web).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')


if __name__ == '__main__':
    main(sys.argv[1:])

