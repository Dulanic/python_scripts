import requests
import json
from datetime import datetime, timedelta

api_key = 'caafe12c153045d9a87d9706130a8073'
url = f'http://tautulli:8181/api/v2?apikey={api_key}&cmd=get_activity'
activity = requests.get(url)
pa = json.loads(activity.text)

sessions = [] 

for session in pa['response']['data']['sessions']:
    sessions.append(session)

  
if len(sessions) == 0:
    print("No current activity")
for session in sessions:
    user = session['user']
    user_email = session['email']
    ip = session['ip_address_public']
    client = session['product']
    audience_rating = session['audience_rating']
    media_type = session['media_type']
    quality = session['quality_profile']
    progress_percent = session['progress_percent']
    title = session['title']
    grandparent_title = session['grandparent_title']
    duration = int(session['duration'])
    resolution = session['video_full_resolution']
    state = session['state']
    full_title = session['full_title']
    size = session['file_size']
    sec = int(duration/1000)
    dur = timedelta(seconds=sec)
    file_size = int(session['file_size'])
    seasonEpisode = 'S' + session['parent_media_index'] + 'E' +session['media_index']
    bw = str(int(session['bitrate'])/1000 )+ 'Mbps'
    ep = session['media_index']
    season = session['parent_media_index']
    print(dur)


