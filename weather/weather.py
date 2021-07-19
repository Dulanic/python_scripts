#!/usr/bin/env python3
import requests
import json
from decouple import config
from db import pguser, pgpass, conn, cur
from datetime import datetime, timedelta, date
import os

def insert_weather():
    insert_query = '''INSERT INTO public.weather (date, temp, dwpt, rhum, prcp, wdir, wspd, pres, updte) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) 
    ON CONFLICT(date)
    DO UPDATE SET
            temp = excluded.temp, dwpt = excluded.dwpt, rhum = excluded.rhum, prcp = excluded.prcp, wdir = excluded.wdir, wspd = excluded.wspd, pres = excluded.pres, updte = excluded.updte;'''
    valuestoinset = (dt, temp, dwpt, rhum, precip, winddir, wspd, pres, updte)
    cur.execute(insert_query, valuestoinset)


def insert_astra():
    insert_query = '''INSERT INTO public.weather_date(
	date, sunrise, sunset,moon_phase, max_temp_f, min_temp_f, totalprecip_in, updte)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT(date)
    DO UPDATE SET
         sunrise = excluded.sunrise, sunset = excluded.sunset, moon_phase = excluded.moon_phase, max_temp_f = excluded.max_temp_f, min_temp_f = excluded.min_temp_f, totalprecip_in = excluded.totalprecip_in, updte = excluded.updte;'''
    valuestoinset = (date, sunrise, sunset, moon_phase, max_temp_f, min_temp_f, totalprecip_in, updte)
    cur.execute(insert_query, valuestoinset)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# Set Date values
hr = 0
h = 0
curr_hr = datetime.now().hour
end_date = date.today() + timedelta(1)
start_date = date.today() - timedelta(6)

# Set API values
ak = config('ak')
city = config('city')

myclient = pymongo.MongoClient("mongodb://192.168.2.155:27017/")
mydb = myclient["weather"]
mycol = mydb["core"]

fn = os.path.basename(__file__)
# Loop through dates
for single_date in daterange(start_date, end_date):
    histurl = 'https://api.weatherapi.com/v1/history.json?key=' + \
        ak + '&q=' + city + '&dt=' + single_date.strftime("%Y-%m-%d")

    r = requests.get(histurl)
    wjson = json.loads(r.text)

    # Insert the astral data for that day
    date = wjson['forecast']['forecastday'][0]['date']
    sunrise = wjson['forecast']['forecastday'][0]['astro']['sunrise']
    sunset = wjson['forecast']['forecastday'][0]['astro']['sunrise']
    moonrise = wjson['forecast']['forecastday'][0]['astro']['moonrise']
    moonset = wjson['forecast']['forecastday'][0]['astro']['moonset']
    moon_phase = wjson['forecast']['forecastday'][0]['astro']['moon_phase']
    max_temp_f = wjson['forecast']['forecastday'][0]['day']['maxtemp_f']
    min_temp_f = wjson['forecast']['forecastday'][0]['day']['mintemp_f']
    totalprecip_in = wjson['forecast']['forecastday'][0]['day']['totalprecip_in']
    avghumidity = wjson['forecast']['forecastday'][0]['day']['avghumidity']
    maxwind_mph = wjson['forecast']['forecastday'][0]['day']['maxwind_mph']
    updte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_astra()

    # Loop through the 24 hours of the day
    for i in wjson['forecast']['forecastday'][0]['hour']:
        updte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        h += 1
        dt = i['time']
        time = datetime.strptime(i['time'][11:16], '%H:%M').time()
        temp = i['temp_f']
        dwpt = i['dewpoint_f']
        rhum = i['humidity']
        precip = i['precip_in']
        winddir = i['wind_dir']
        wspd = i['wind_mph']
        pres = i['pressure_mb']
        if datetime.strptime(dt, '%Y-%m-%d %H:%M') >= datetime.combine(end_date, time):
            break
        insert_weather()

# Commit to DB
conn.commit()

now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

print(f"{dt_string} - {fn} - {h} record(s) inserted successfully into weather table")
conn.close()