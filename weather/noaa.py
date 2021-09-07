#!/usr/bin/env python
from noaa_sdk import NOAA
import json 
import pymongo 
from datetime import date
import dateutil.relativedelta

today = date.today()
onemonthago = today - dateutil.relativedelta.relativedelta(months=1)
format = "%Y-%m-%d"

myclient = pymongo.MongoClient('mongodb://192.168.2.155:27017/')
mydb = myclient['weather']
mycol = mydb['noaa']

n = NOAA()
observations = n.get_observations('75077','US', start=onemonthago.strftime(format), end=today.strftime(format) )

for observation in observations:
    w = json.loads(json.dumps(observation))
    g =  mycol.update_one({'timestamp': w['timestamp']}, {'$set': w}, upsert=True)
