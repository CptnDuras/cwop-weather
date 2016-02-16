import urllib2
import json
from datetime import datetime
from time import strptime, mktime, strftime
from bs4 import BeautifulSoup
from flask import Flask, render_template

my_call = 'KG7NXM'

station = 'DW5092'

# 20160215134853
# 2016-02-15-13:48:53
in_time_format = '%Y%m%d%H%M%S'
out_time_format = "%a, %d %b %Y %H:%M:%S"


def get_weather_data(station):
    data = {}
    weather_data_uri = 'http://www.findu.com/cgi-bin/wxxml.cgi?call=%s&last=24' % station

    request = urllib2.urlopen(weather_data_uri)
    response = request.read()

    pretty_response = BeautifulSoup(response, 'xml')

    for line in pretty_response.find_all("weatherReport"):
        report = {child.name: child.text for child in line.findChildren()}
        report['pretty_time'] = datetime.fromtimestamp(mktime(strptime(report['timeReceived'],
                                                                       in_time_format))).strftime(out_time_format)

        data[report['timeReceived']] = report

    print data
    return data

weather_data = get_weather_data(station)



app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/data')
@app.route('/data/')
def get_all_weather_data():
    data = get_weather_data(station)
    return json.dumps(data)


@app.route('/data/<time>')
def get_weather_data_for_time(time):
    data = get_weather_data(station)

    return json.dumps(data[time])


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



if __name__ == '__main__':
    app.run(debug=True)