from flask import request
from flask import Flask, render_template
from flask import Response
import time
from dao.ExternalContentDao import ExternalContentDao
from dao.PublicServerDao import PublicServerDao

import simplejson as json
import datetime
import decimal
app = Flask(__name__)
app.debug = True
externalContent = ExternalContentDao()
serverDao = PublicServerDao()


def verify_token(password):
    passw = 'thisisourtoken'
    if password == passw:
        return True
    return False


@app.route('/')
def weather():
    weather_data = {"forecasts": [externalContent.get_marine_forecast(externalContent.HOWE_SOUND),
                                  externalContent.get_marine_forecast(externalContent.GEORGIA_SOUTH)],
                    "current_conditions": [externalContent.get_marine_conditions(externalContent.PAM_ROCKS),
                                           externalContent.get_marine_conditions(externalContent.POINT_ATKINSON),
                                           externalContent.get_marine_conditions(externalContent.HALIBUT_BANK)],
                    "tide_locations": [externalContent.POINT_ATKINSON, externalContent.GIBSONS],
                    "config_title": "Bowen Island Marine Weather"}
    __log_access()
    return render_template("weather.html", weather_data=weather_data)


@app.route('/custom')
def custom_weather():
    forecast_areas = json.loads(request.values.get("forecasts"))
    forecasts = []
    for forecast_area in forecast_areas:
        forecasts.append(externalContent.get_marine_forecast(forecast_area))

    condition_stations = json.loads(request.values.get("conditions"))
    conditions = []
    for condition_station in condition_stations:
        conditions.append(externalContent.get_marine_conditions(condition_station))

    tide_stations = json.loads(request.values.get("tides"))
    title = request.values.get("title")
    if not title:
        title = "Custom Marine Weather"
    weather_data = {"forecasts": forecasts,
                    "current_conditions": conditions,
                    "tide_locations": tide_stations,
                    "config_title": title}
    __log_access()
    return render_template("weather.html", weather_data=weather_data)


@app.route('/buildUrl')
def build_url():
    stations = {"forecast_areas": externalContent.get_forecast_areas(),
                "tide_stations": externalContent.get_tide_stations(),
                "condition_stations": {
                    "land": externalContent.get_condition_stations("land"),
                    "buoy": externalContent.get_condition_stations("buoy")
                    }
                }
    build_base_url = request.base_url.replace("buildUrl", "custom")
    __log_access()
    return render_template("marineWxBuilder.html", station_data=stations, base_url=build_base_url)


@app.route('/getConditionStations')
def get_condition_stations():
    station_type = request.args.get('stationType')
    stations = externalContent.get_condition_stations(station_type)
    return Response(response=json.dumps(stations),
                    status=200,
                    mimetype="application/json")


@app.route('/getTideStations')
def get_tide_stations():
    return Response(response=json.dumps(externalContent.get_tide_stations()),
                    status=200,
                    mimetype="application/json")


@app.route('/getForecastAreas')
def get_forecast_areas():
    return Response(response=json.dumps(externalContent.get_forecast_areas()),
                    status=200,
                    mimetype="application/json")


@app.route('/getMarineConditions')
def current_marine_condition():
    try:
        station = request.args.get('station')
        obj = externalContent.get_marine_conditions(station)
        return Response(response=json.dumps(obj),
                        status=200,
                        mimetype="application/json")
    except ValueError:
        return Response(response=json.dumps({"error": "Invalid station name. Use /weather/getConditionStations for valid names."}),
                        status=200,
                        mimetype="application/json")


@app.route('/getMarineForecast')
def current_marine_forecast():
    try:
        area = request.args.get('area')
        obj = externalContent.get_marine_forecast(area)
        return Response(response=json.dumps(obj),
                        status=200,
                        mimetype="application/json")
    except ValueError:
        return Response(response=json.dumps({"error": "Invalid area name. Use /weather/getConditionStations for valid names."}),
                        status=200,
                        mimetype="application/json")

@app.route('/getTides')
def get_tides():
    try:
        location_name = request.args.get("location_name")
        tide_data = externalContent.get_tides(location_name, datetime.date.today())
        data = {"success": True, "tide_data": tide_data}
        return Response(response=json.dumps(data),
                        status=200,
                        mimetype="application/json")
    except ValueError:
        data = {"success": False}
        return Response(response=json.dumps(data),
                        status=200,
                        mimetype="application/json")


def __log_access():
    try:
        log_data = {"remote_address": request.remote_addr, "url": request.url}
        serverDao.log_access(env_data=log_data)
    except Exception as e:
        print("Could not log access.")
        print(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
