#!/usr/bin/env python
from noaa_sdk import NOAA
import json 
import pymongo 
from datetime import date, datetime
from zoneinfo import ZoneInfo
import dateutil.relativedelta
import os


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


myclient = pymongo.MongoClient('mongodb://192.168.2.155:27017/')
mydb = myclient['weather']
mycol = mydb['noaa']
n = NOAA()
observations = n.get_observations('75077','US')


for observation in observations:
    ct += 1
    w = json.loads(json.dumps(observation))
    g =  mycol.update_one({'timestamp': w['timestamp']}, {'$set': w}, upsert=True)
    if g.matched_count == 1 and g.modified_count == 0:
        mat += 1
    elif g.matched_count == 0 and g.modified_count == 1:
        upd += 1
    elif g.matched_count == 0 and g.modified_count == 0: 
        ins +=1


print(f'{ts()} - {fn} - Inserted {ins} and Updated {upd} out of {ct} weather records.')