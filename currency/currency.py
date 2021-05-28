import requests
import os
import json
import pymongo
from datetime import datetime, timedelta, date

myclient = pymongo.MongoClient("mongodb://192.168.2.155:27017/")
mydb = myclient["currency"]
mycol = mydb["history"]
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
fn = os.path.basename(__file__)

url = 'https://api.exchangerate.host/latest?base=USD'
r = requests.get(url)
currency = json.loads(r.text)
b = currency[0]
try:
    ins = mycol.update_one(
        {'date': currency['date']}, {'$set': currency}, upsert=True)
    if ins.matched_count == 0:
        print(f"{dt_string} - {fn} - 1 record(s) inserted successfully into weather table")
except Exception as e:
    print(f"{dt_string} - {fn} - An exception occurred :: {e}")
