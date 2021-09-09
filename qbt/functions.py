from datetime import datetime
from zoneinfo import ZoneInfo
import qbittorrentapi

def ts():
    date_time = datetime.now().astimezone(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d %H:%M:%S")
    return date_time
    
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

qbt_client = qbittorrentapi.Client(host='192.168.2.155', port=8089)
