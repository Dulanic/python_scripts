from noaa_sdk import NOAA
import json 
#import requests
#from decouple import config
#from datetime import datetime, timedelta, date
import pymongo 
f = []
myclient = pymongo.MongoClient('mongodb://192.168.2.155:27017/')
mydb = myclient['weather']
mycol = mydb['test']

n = NOAA()
observations = n.get_observations('75077','US', start='2021-01-01', end='2021-06-14' )

for observation in observations:
    w = json.loads(json.dumps(observation))
    g =  mycol.update_one({'timestamp': w['timestamp']}, {'$set': w}, upsert=True)