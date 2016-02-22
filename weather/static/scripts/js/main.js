function refresh_weather( callback){
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", '/refresh_data', true); // true for asynchronous
    xmlHttp.send(null);
}

var source = new EventSource('/subscribe');
source.onmessage = function (event) {
    var data=JSON.parse(event.data);

    var columnSet = [];
    for (var key in data) {
        var element_key = "#weather_" + key;
        var element = $(element_key);
        console.log("key:\t" + key);
        console.log("element_key:\t" + element_key);
        console.log("element:\t" + element);
        console.log("data[key]:\t" + data[key]);

        element.html(data[key]);

    }
};


