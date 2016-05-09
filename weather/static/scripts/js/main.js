var temp_chart_id = "#temperatureChart";
var ctx = $(temp_chart_id).get(0).getContext("2d");

function refresh_weather(){
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            console.log(xmlHttp.responseText)
        }
    };

    xmlHttp.open("GET", '/refresh_data', true); // true for asynchronous
    xmlHttp.send(null);
}


var source = new EventSource('/subscribe');
source.onmessage = function(event) {
    var data=JSON.parse(event.data);

    for(var key in data) {
        var element_key = "#weather_" + key;
        var element = $(element_key);

        //console.log("key:\t" + key);
        //console.log("element_key:\t" + element_key);
        //console.log("element:\t" + element);
        //console.log("data[key]:\t" + data[key]);

        element.html(data[key]);

    }
};

function refresh_temp_chart(){
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            var data=JSON.parse(xmlHttp.responseText);

            var myNewChart = new Chart(ctx).Line(data, {bezierCurve: false});
        }
    };

    xmlHttp.open("GET", '/chart_temp_data', true); // true for asynchronous
    xmlHttp.send(null);
}
