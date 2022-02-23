#!/usr/bin/env python
from noaa_sdk import NOAA
import json 
import pymongo 
from datetime import date, datetime
from zoneinfo import ZoneInfo
import dateutil.relativedelta
import os


def insert_weather():
    insert_query = '''INSERT INTO public.noaa(
	__id, _type, "barometricPressure.qualityControl", "barometricPressure.unitCode", "barometricPressure.value", "dewpoint.qualityControl", "dewpoint.unitCode", "dewpoint.value	", "elevation.unitCode	", "elevation.value	", "heatIndex.qualityControl	", "heatIndex.unitCode	", "heatIndex.value	", "icon	", "maxTemperatureLast24Hours.qualityControl	", "maxTemperatureLast24Hours.unitCode	", "maxTemperatureLast24Hours.value	", "minTemperatureLast24Hours.qualityControl	", "minTemperatureLast24Hours.unitCode	", "minTemperatureLast24Hours.value	", "precipitationLast3Hours.qualityControl	", "precipitationLast3Hours.unitCode	", "precipitationLast3Hours.value	", "precipitationLast6Hours.qualityControl	", "precipitationLast6Hours.unitCode	", "precipitationLast6Hours.value	", "precipitationLastHour.qualityControl	", "precipitationLastHour.unitCode	", "precipitationLastHour.value	", "rawMessage	", "relativeHumidity.qualityControl	", "relativeHumidity.unitCode	", "relativeHumidity.value	", "seaLevelPressure.qualityControl	", "seaLevelPressure.unitCode	", "seaLevelPressure.value	", "station	", "temperature.qualityControl	", "temperature.unitCode	", "temperature.value	", "textDescription	", datetime, "visibility.qualityControl	", "visibility.unitCode	", "visibility.value	", "windChill.qualityControl	", "windChill.unitCode	", "windChill.value	", "windDirection.qualityControl	", "windDirection.unitCode	", "windDirection.value	", "windGust.qualityControl	", "windGust.unitCode	", "windGust.value	", "windSpeed.qualityControl	", "windSpeed.unitCode	", "windSpeed.value	")
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ?);
    ON CONFLICT(date)
    DO UPDATE SET
            temp = excluded.temp, dwpt = excluded.dwpt, rhum = excluded.rhum, prcp = excluded.prcp, wdir = excluded.wdir, wspd = excluded.wspd, pres = excluded.pres, updte = excluded.updte;'''
    valuestoinset = (dt, temp, dwpt, rhum, precip, winddir, wspd, pres, updte)
    cur.execute(insert_query, valuestoinset)

def ts():
    date_time = datetime.now().astimezone(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d %H:%M:%S")
    return date_time

today = date.today()
fn = os.path.basename(__file__)
onemonthago = today - dateutil.relativedelta.relativedelta(months=1)
format = "%Y-%m-%d"
ins = 0
upd = 0
mat = 0
ct = 0

n = NOAA()
observations = n.get_observations('75077','US')


for observation in observations:
    id = observation['@id']
    typ = observation['@type']
    elvuc = observation['elevation']['unitCode']
    elvval = observation['elevation']['value']
    station = observation['station']
    datetime = observation['timestamp']
    rawMessage = observation['rawMessage']
    weather_desc = observation['textDescription']
    weather_icon = observation['icon']
    temp_code = 'C' if 'degC' in observation['temperature']['unitCode'] else ''
    temp_val = observation['temperature']['value']
    dew_val = observation['dewpoint']['value']



print(f'{ts()} - {fn} - Inserted {ins} and Updated {upd} out of {ct} weather records.')