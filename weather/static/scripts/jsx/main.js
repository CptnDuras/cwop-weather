var WeatherInfo = React.createClass({
    render: function(){
        return(
            <div className="col-md-5">
                <table className="table">
                    <tbody>
                        <tr>
                            <td>Date/Time received:</td>
                            <td>Temperature:</td>
                            <td>Barometric Pressure:</td>
                            <td>Humidity:</td>
                        </tr>
                        <tr>
                            <td>{this.props.pretty_time}</td>
                            <td>{this.props.temperature}</td>
                            <td>{this.props.barometer}</td>
                            <td>{this.props.humidity}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        )
    }
});
var WeatherData = React.createClass({
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
            return <WeatherInfo pretty_time={data.pretty_time} temperature={data.temperature} humidity={data.humidity} barometer={data.barometer} />
        });
        return (
            <div>
                <button onClick={this.handleClick}>Refresh</button>
                {weather_info}
            </div>
        );
    }
});

ReactDOM.render(
    <WeatherData />,
    document.getElementById('content')
);