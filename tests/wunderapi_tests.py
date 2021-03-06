from nose.tools import assert_equals, assert_equal
from weather.weather import Weather
import json


def setup(location=None, units=None, date=None):
    return Weather(location=location, units=units, date=date,
                   config_file='tests/resources/config')


def mock_result(mockfile='tests/resources/conditions.txt'):
    with open(mockfile) as data_file:
            result = json.load(data_file)
    return result


def mock_date_result():
    with open('tests/resources/forecast.txt') as data_file:
            result = json.load(data_file)
    data = result['forecast']['simpleforecast']['forecastday']
    for item in data:
        date = item['date']
    return date


def mock_forecast_result():
    with open('tests/resources/forecast.txt') as data_file:
            result = json.load(data_file)
    return result


def setup_metric():
    return Weather(config_file='tests/resources/config', units='metric')

def test_passed_location_overrides_config():
    api = setup(location=27695)
    assert_equals(api.get_url('conditions'),
                  "http://api.wunderground.com/api/%s/conditions/q/%s.json" %
                  (api.config.api_key, "27695"))


def test_get_temp_f():
    api = setup()
    assert_equals(("66.3%sF" % u"\u00b0"), api.get_temp(mock_result()))


def test_get_temp_c():
    api = setup(units="metric")
    assert_equals(("19.1%sC" % u"\u00b0"), api.get_temp(mock_result()))


def test_get_url_current():
    api = setup()
    assert_equals(api.get_url('conditions'),
                  "http://api.wunderground.com/api/%s/conditions/q/%s.json" %
                  (api.config.api_key, api.config.location))


def test_get_conditions_english():
    api = setup()
    conditions = "\nCurrent weather for San Francisco, CA \n"
    conditions += "66.3\u00b0F and Partly Cloudy \n"
    conditions += "Winds: From the NNW at 22.0 MPH Gusting to 28.0 MPH \n"
    conditions += "Relative Humidity: 65%\n"
    assert_equal(conditions, api.get_conditions(mock_result()))


def test_get_conditions_metric():
    api = setup_metric()
    conditions = "\nCurrent weather for San Francisco, CA \n"
    conditions += "19.1\u00b0C and Partly Cloudy \n"
    conditions += "Winds: From the NNW at 35.4 KPH Gusting to 45.1 KPH \n"
    conditions += "Relative Humidity: 65%\n"
    assert_equal(conditions, api.get_conditions(mock_result()))


def test_get_is_dict():
    api = setup()
    assert isinstance(api.get_result('conditions'), dict)


def test_get_forecast_short():
    api = setup()
    forecast = []
    forecast.append(['Date', 'Condition', 'Rain Chance',
                     'Temp Hi/Lo', 'Wind', 'Humidity'])
    forecast.append(['June 26', 'Partly Cloudy', '0%',
                     '68°F / 50°F', '17 MPH', '72%'])
    forecast.append(['June 27', 'Partly Cloudy', '0%',
                     '72°F / 54°F', '9 MPH', '70%'])
    forecast.append(['June 28', 'Partly Cloudy', '0%',
                     '72°F / 54°F', '12 MPH', '80%'])
    forecast.append(['June 29', 'Fog', '0%',
                     '68°F / 52°F', '10 MPH', '79%'])
    assert_equal(forecast, api.get_forecast(mock_forecast_result()))


def test_format_date_date():
    api = setup()
    assert_equals("June 29", api.format_date(mock_date_result()))


def test_format_date_date_empty():
    api = setup()
    assert_equals("June 29", api.format_date(mock_date_result()))


def test_format_date_day():
    api = setup(date="day")
    assert_equals("Friday", api.format_date(mock_date_result()))


def test_passed_date_overides_config():
    api = setup(date="day")
    assert_equals("Friday", api.format_date(mock_date_result()))


def test_format_wind_english():
    api = setup()
    result = mock_forecast_result()
    result = result['forecast']['simpleforecast']['forecastday'][0]
    assert_equals("17 MPH", api.format_wind(result))


def test_format_wind_metric():
    api = setup_metric()
    result = mock_forecast_result()
    result = result['forecast']['simpleforecast']['forecastday'][0]
    assert_equals("27 KPH", api.format_wind(result))


def test_format_temp_english():
    api = setup()
    result = "66.3"
    assert_equals(("66.3%sF" % u"\u00b0"), api.format_temp(result))


def test_format_temp_metric():
    api = setup_metric()
    result = "19.1"
    assert_equals(("19.1%sC" % u"\u00b0"), api.format_temp(result))


def test_format_date_day_short():
    api = setup(date="shortday")
    assert_equals("Fri", api.format_date(mock_date_result()))


def test_get_wind_string_english():
    api = setup()
    assert_equal("From the NNW at 22.0 MPH Gusting to 28.0 MPH",
                 api.get_wind_string(mock_result()))

def test_get_wind_string_calm():
    api = setup()
    assert_equal("Calm",
                 api.get_wind_string(mock_result(
                     mockfile="tests/resources/conditions_calm.txt")))

def test_get_wind_string_metric():
    api = setup_metric()
    assert_equal("From the NNW at 35.4 KPH Gusting to 45.1 KPH",
                 api.get_wind_string(mock_result()))
