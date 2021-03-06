#!/usr/bin/python
import requests
import json
from decouple import config
from datetime import datetime, timedelta, date
import pymongo

ak1 = config('ak1')
lat = config('lat')
lon = config('lon')

myclient = pymongo.MongoClient('mongodb://192.168.2.155:27017/')
mydb = myclient['weather']
mycol = mydb['hourly']

start_dt = datetime.now() + timedelta(hours=-120)

for single_date in (start_dt + timedelta(n) for n in range(6)):
    time_object = str(single_date.timestamp())[0:10]
    url = \
        'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=' \
        + lat + '&lon=' + lon + '&dt=' + time_object + '&appid=' + ak1 \
        + '&units=imperial'
    r = requests.get(url)
    wjson = json.loads(r.text.replace('1h','rain1h'))

    for row in wjson['hourly']:
        a = row
        i = mycol.update_one({'dt': row['dt']}, {'$set': row}, upsert=True)