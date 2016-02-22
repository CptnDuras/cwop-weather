#!/usr/bin/python
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from weather import app

app.debug = True
server = WSGIServer(("", 5000), app)
server.serve_forever()
