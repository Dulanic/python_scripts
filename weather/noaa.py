#!/usr/bin/env python
from noaa_sdk import NOAA
import json 
import pymongo 
from datetime import date, datetime
import dateutil.relativedelta
import sys, os


def ts():
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date_time

today = date.today()
fn = os.path.basename(__file__)
onemonthago = today - dateutil.relativedelta.relativedelta(months=1)
format = "%Y-%m-%d"
ct = 0

myclient = pymongo.MongoClient('mongodb://192.168.2.155:27017/')
mydb = myclient['weather']
mycol = mydb['noaa']
n = NOAA()
observations = n.get_observations('75077','US', start=onemonthago.strftime(format), end=today.strftime(format) )


for observation in observations:
    w = json.loads(json.dumps(observation))
    g =  mycol.update_one({'timestamp': w['timestamp']}, {'$set': w}, upsert=True)

print(f'{ts()} - {fn} - Updated {ct} weather records.')