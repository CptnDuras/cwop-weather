import urllib2
from datetime import datetime
from time import strptime, mktime
from bs4 import BeautifulSoup


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

        data[int(report['timeReceived'])] = report

    # print data
    return data
