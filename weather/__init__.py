from flask import Flask
from flask_influxdb import InfluxDB
import gevent
from gevent.queue import Queue

def load_views():
    from weather import views


def load_models():
    from weather import models





app = Flask(__name__)
app.config.from_pyfile('config.py')
app.subscriptions = []

influx_db = InfluxDB(app)
load_views()
