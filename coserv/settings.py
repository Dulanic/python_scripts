#!/usr/bin/env python3
from sys import platform
from decouple import config
from typing import NamedTuple, List
import os
import glob
import datetime
from dotenv import load_dotenv
load_dotenv()


def find_files(filename, search_path):
   result = glob.glob(search_path + '/**/' + filename, recursive = True)
   return result

def timestamp():
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string
    
def cleardir(path):
    files = glob.glob(path + '*')
    for f in files: 
        os.remove(f)

class ConfigSet(NamedTuple):
    url = os.environ.get('csrvurl')
    url_trail = os.environ.get('url_trail')
    clogin = os.environ.get('clogin')
    cpass = os.environ.get('cpass')
    nn = "coserv.csv"
    #If for download location 
    if platform in ("linux","linux2"):
        dl_folder = "/coserv/"
    elif platform == "win32":
        dl_folder = 'C:\\coserv\\'
    #File location
    if platform in ("linux","linux2"):
        file_loc = "/coserv/coserv.csv"
    elif platform == "win32":
        file_loc = 'C:\\coserv\\coserv.csv'
    #File location
    if platform in ("linux","linux2"):
        tmp_file_loc = "/coserv/coservtmp.csv"
    elif platform == "win32":
        tmp_file_loc = 'C:\\coserv\\coservtmp.csv'
    
