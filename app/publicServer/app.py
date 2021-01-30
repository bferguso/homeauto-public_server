from flask import request
from flask import Flask, render_template
from flask import Response
import time
from dao.ExternalContentDao import ExternalContentDao

import simplejson as json
import datetime
import decimal
app = Flask(__name__)
app.debug = True
externalContent = ExternalContentDao()


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
                    "tide_data": [externalContent.get_tides(externalContent.POINT_ATKINSON, datetime.date.today()),
                                  externalContent.get_tides(externalContent.GIBSONS, datetime.date.today())]}
    return render_template("weather.html", weather_data=weather_data)


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
    station = request.args.get('station')
    obj = externalContent.get_marine_conditions(station)
    return Response(response=json.dumps(obj),
                    status=200,
                    mimetype="application/json")


@app.route('/getMarineForecast')
def current_marine_forecast():
    area = request.args.get('area')
    obj = externalContent.get_marine_forecast(area)
    return Response(response=json.dumps(obj),
                    status=200,
                    mimetype="application/json")


@app.route('/getTides')
def tides():
    station = request.args.get('station')
    obj = externalContent.get_tides(station, datetime.date.today())
    return Response(response=json.dumps(obj),
                    status=200,
                    mimetype="application/json")

def tideStationList():
    externalContent.S


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
