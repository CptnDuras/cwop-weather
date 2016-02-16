(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var WeatherInfo = React.createClass({displayName: "WeatherInfo",
    render: function(){
        return(
            React.createElement("div", {className: "col-md-5"}, 
                React.createElement("table", {className: "table"}, 
                    React.createElement("tbody", null, 
                        React.createElement("tr", null, 
                            React.createElement("td", null, "Date/Time received:"), 
                            React.createElement("td", null, "Temperature:"), 
                            React.createElement("td", null, "Barometric Pressure:"), 
                            React.createElement("td", null, "Humidity:")
                        ), 
                        React.createElement("tr", null, 
                            React.createElement("td", null, this.props.pretty_time), 
                            React.createElement("td", null, this.props.temperature), 
                            React.createElement("td", null, this.props.barometer), 
                            React.createElement("td", null, this.props.humidity)
                        )
                    )
                )
            )
        )
    }
});
var WeatherData = React.createClass({displayName: "WeatherData",
    getInitialState: function() {
        return {
            weather_data: []
        }
    },

    fetchWeather: function() {

        $.getJSON("/current", function(result) {
            var data = result;

            this.state.weather_data.push({pretty_time: data.pretty_time, temperature: data.temperature, humidity: data.humidity, barometer: data.barometer});
            this.setState({
                weather_data: this.state.weather_data
            });
        }.bind(this));
    },

    generateWeatherData: function() {
        [1].map(function() {
            this.fetchWeather();
        }.bind(this));
    },

    componentDidMount: function() {
        this.fetchWeather();
    },

    handleClick: function(e) {
        e.preventDefault();
        this.setState({weather_data: []});
        this.fetchWeather();
    },

    render: function() {
        var weather_info = this.state.weather_data.map(function(data) {
            return React.createElement(WeatherInfo, {pretty_time: data.pretty_time, temperature: data.temperature, humidity: data.humidity, barometer: data.barometer})
        });
        return (
            React.createElement("div", null, 
                React.createElement("button", {onClick: this.handleClick}, "Refresh"), 
                weather_info
            )
        );
    }
});

ReactDOM.render(
    React.createElement(WeatherData, null),
    document.getElementById('content')
);

},{}]},{},[1])