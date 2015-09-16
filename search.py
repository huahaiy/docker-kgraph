#!/usr/bin/python

import sys, getopt 
import numpy as np
import pykgraph as kg
import json

from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.routing import url
from wheezy.web.handlers import BaseHandler
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory

class SearchHandler(BaseHandler):

    def get(self):
	# TODO: check the params exist and validate them, also allow specifying data 
	#d = self.request.query.get('d')[0]
	k = int(self.request.query.get('k')[0])
	q = [[float(x) for x in self.request.query.get('q')]]

    	pq = np.zeros((1, n - 1 + needed))
	pq[:, :-needed] = q

	result = index.search(padded, pq, K = k, withDistance = True)

        return self.json_response({'ids': result[0][0].tolist(), 'dists': result[1][0].tolist()})


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

def main(argv):
    # TODO: load multiple data files and indices
    datafile = ''
    port = 8071

    try:
        opts, args = getopt.getopt(argv, "hp:f:", ["port=", "datafile="])
    except getopt.GetoptError:
        print 'search.py -p <port> -f <datafile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'search.py -p <port> -f <datafile>'
            sys.exit()
        elif opt in ("-f", "--datafile"):
            datafile = arg
	elif opt in ("-p", "--port"):
	    port = arg

    global n, needed, padded, index

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

    from wsgiref.simple_server import make_server
    try:
        print('Server started on port ' + str(port))
        make_server('', port, web).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')


if __name__ == '__main__':
    main(sys.argv[1:])

