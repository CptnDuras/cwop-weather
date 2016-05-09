from weather import app, influx_db
from weather.methods import get_weather_data, station
from flask import render_template, Flask, Response
from pyxley import UILayout
# from pyxley.filters import SelectButton
# from pyxley.charts.mg import LineChart, Figure, ScatterPlot, Histogram
# from pyxley.charts.datatables import DataTable
import json
import gevent
from gevent.queue import Queue


TITLE = 'Weather'

title_scripts = [

]
scripts = [
    "./components/jquery/dist/jquery.js",
    "./scripts/js/main.js",
    "./components/Chart.js/Chart.js",
    "./components/react/react.js",
    "./components/react/react-dom.js",
    "./components/bootstrap/dist/js/bootstrap.js",
]

css = [
    "./components/bootstrap/dist/css/bootstrap.css"
]

# Make a UI
ui = UILayout(
    "FilterChart",
    "./static/bower_components/pyxley/build/pyxley.js",
    "component_id",
    filter_style="''")


# ServerSentEvent SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data: "data",
            self.event: "event",
            self.id: "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k)
                 for k, v in self.desc_map.iteritems() if k]

        return "%s\n\n" % "\n".join(lines)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title=TITLE,
                           title_scripts=title_scripts,
                           scripts=scripts,
                           css=css)


@app.route('/data')
@app.route('/data/')
def get_all_weather_data():
    data = get_weather_data(station)
    return json.dumps(data)


@app.route('/data/<time>')
def get_weather_data_for_time(time):
    data = get_weather_data(station)

    return json.dumps(data[time])


@app.route('/station/<stationid>')
def set_weather_station(stationid):
    station = stationid

    return station

@app.route('/current')
def get_current_data():
    data = get_weather_data(station)

    latest = json.dumps(data[max(data)])

    return latest


@app.route('/current/<stat>')
def get_current_stat(stat):
    data = get_weather_data(station)

    latest = data[max(data)][stat]

    return latest

@app.route('/refresh_data')
def refresh_data():
    def notify():
        data = get_weather_data(station)
        msg = json.dumps(data[max(data)])

        for sub in app.subscriptions[:]:
            sub.put(msg)

    try:
        gevent.spawn(notify)
        return "OK"
    except:
        return "NOT OK"

# Event stream route
@app.route('/subscribe')
def subscribe():
    def gen():
        q = Queue()
        app.subscriptions.append(q)
        try:
            while True:
                result = q.get()
                event = ServerSentEvent(str(result))
                yield event.encode()
        except GeneratorExit:
            app.subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")


@app.route('/chart_temp_data')
def get_chart_temp_data():
    #     temp_data = {
    #     labels: ["January", "February", "March", "April", "May", "June", "July"],
    #     datasets: [
    #         {
    #             label: "My First dataset",
    #             fillColor: "rgba(220,220,220,0.2)",
    #             strokeColor: "rgba(220,220,220,1)",
    #             pointColor: "rgba(220,220,220,1)",
    #             pointStrokeColor: "#fff",
    #             pointHighlightFill: "#fff",
    #             pointHighlightStroke: "rgba(220,220,220,1)",
    #             data: [65, 59, 80, 81, 56, 55, 40]
    #         }
    #     ]
    # };
    data = get_weather_data(station)
    sorted_data = sorted(data)
    out_data = []
    out_labels = []


    for key in sorted_data:
        out_labels.append(data[key]['pretty_time'])
        out_data.append(data[key]['temperature'])


    out_json = {
        'labels': out_labels,
        'datasets': [{
            'label': "Temperature",
            'fillColor': "rgba(220,220,220,0.2)",
            'strokeColor': "rgba(220,220,220,1)",
            'pointColor': "rgba(220,220,220,1)",
            'pointStrokeColor': "#fff",
            'pointHighlightFill': "#fff",
            'pointHighlightStroke': "rgba(220,220,220,1)",
            'data': out_data
        }]
    }

    return json.dumps(out_json)