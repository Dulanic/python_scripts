#!/usr/bin/python3
import os
import qbittorrentapi
from functions import ts, sizeof_fmt, qbt_client
from collections import Counter
from urllib.parse import urlparse

def tracker_convert(tracker):
    a = trdict.get(tracker)
    return a

def reason_str(reason_num, age, ratio):
    reason_dict = {
        1: f"due to bad tracker",
        2: f"due to seeding for {age} days",
        3: f"due to seeding for {age} days and {ratio} ratio",
        4: f"due to seeding ratio of {ratio}"
    }

    b = reason_dict.get(reason_num)
    return b


trdict = {
  "localhost.stackoverflow.tech": "IPT",
  "tracker.beyond-hd.me": "BHD",
  "ssl.empirehost.me": "IPT",
  "routing.bgp.technology": "IPT",
  "tracker.gazellegames.net": "GGT",
  "tracker.privatehd.to": "PHD",
  "tracker.tleechreload.org": "TL",
  "tracker.torrentleech.org": "TL",
  "speed.connecting.center": "SCD",
  "tracker.tv-vault.me": "TVV", 
  "tracker.cinemaz.to": "CIN",
  "tracker.pixelhd.me": "PIX",
  "abtorrents.me": "ABM",
  "tt.jumbohostpro.eu": "PHD",
  "tracker.alpharatio.cc": "AR",
  "t.connecting.center": "PHD"
}

# Trackers not to be excluded
tr_exclude = [
    'TVV',
    'GGT',
    'ABM'
]

fn = os.path.basename(__file__)
torrent_list = [] 
torrent_list_to_check = [] 
del_ct = 0 
del_size = 0 
torrent_list_file_size = 0 
torrent_list_ct = []
hash_list_to_delete = [] 

for t in qbt_client.torrents_info():
    torrent_list_ct.append(tracker_convert(urlparse(t.tracker).hostname))
    for i in t.trackers:
        for u in str(i.tier):
            if u.isnumeric():
                r = qbt_client.torrents_files(hash=t.hash)
                torrent = [t.hash,t.size,t.name,tracker_convert(urlparse(t.tracker).hostname),1,t.ratio,t.category,t.num_seeds,t.seeding_time/86400]
                torrent_list.append(torrent) if torrent not in torrent_list else torrent_list
                torrent_list_file_size += t.size
                torrent_list_to_check.append(torrent) if i.msg in ('unregistered torrent','Torrent is not found or it is awaiting moderation','002: Invalid InfoHash, Torrent not found') and torrent not in torrent_list_to_check else torrent_list_to_check 
    torrent = [t.hash,t.size,t.name,tracker_convert(urlparse(t.tracker).hostname),3,t.ratio,t.category,t.num_seeds,t.seeding_time/86400]
    #if torrent[3] == None:
    #    print(torrent)
    if (t.ratio > 2 and t.category == 'archive' and t.seeding_time > (60*60*24*30)):
        torrent_list_to_check.append(torrent) if torrent not in torrent_list_to_check else torrent_list_to_check
    elif t.seeding_time > 7776000:
        torrent_list_to_check.append(torrent) if torrent not in torrent_list_to_check else torrent_list_to_check
    elif t.ratio > 10: # delete if > 2.0 and in archive or if 30+ days old 
        torrent_list_to_check.append(torrent) if torrent not in torrent_list_to_check else torrent_list_to_check

trackct = Counter(torrent_list_ct)    #count of items for each tracker   

for rw in torrent_list_to_check:
    tracker, ratio, age, reason_num = rw[3], round(rw[5],2), round(rw[8]), rw[4]
    if tracker not in tr_exclude and trackct[rw[3]] > 2:
        del_reason = reason_str(reason_num, age, ratio) 
        if reason_num == 1 or reason_num in [2,3,4]:
            print(f'{ts()} - {fn} - {rw[2]} has been deleted {del_reason}')
            del_ct += 1
            del_size += rw[1]
            hash_list_to_delete.append(rw[0])

if len(hash_list_to_delete) > 0:
    qbt_client.torrents_delete(torrent_hashes=hash_list_to_delete,delete_files=True)

print(f'{ts()} - {fn} - Scanned a total of {len(torrent_list)} files totalling {sizeof_fmt(torrent_list_file_size)}')

if len(torrent_list_to_check) > 0: 
    print(f'{ts()} - {fn} - Deleted a total of {del_ct} file(s) with a total size of {sizeof_fmt(del_size)}')
else:
    print(f'{ts()} - {fn} - No stale files found to be deleted')
