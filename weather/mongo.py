#!/home/dulanic/python_scripts/weather/venv/bin/python3.10
import requests
import json
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pymongo
import os


def ts():
    date_time = datetime.now().astimezone(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d %H:%M:%S")
    return date_time

ak1 = os.environ.get('ak1')
lat = os.environ.get('lat')
lon = os.environ.get('lon')

fn = os.path.basename(__file__)
myclient = pymongo.MongoClient('mongodb://192.168.2.155:27017/')
mydb = myclient['weather']
mycol = mydb['hourly']
ins = upd = mat = ct = 0

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
        ct += 1
        a = row
        g = mycol.update_one({'dt': row['dt']}, {'$set': row}, upsert=True)
        if g.matched_count == 1 and g.modified_count == 0:
            mat += 1
        elif g.matched_count == 0 and g.modified_count == 1:
            upd += 1
        elif g.matched_count == 0 and g.modified_count == 0: 
            ins +=1


print(f'{ts()} - {fn} - Inserted {ins} and Updated {upd} out of {ct} weather records.')
