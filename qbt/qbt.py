#!/usr/bin/python3
import os
import qbittorrentapi
from functions import ts, sizeof_fmt, qbt_client
from collections import Counter
from urllib.parse import urlparse

def tracker_convert(tracker):
    a = trdict.get(tracker)
    return a

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
#  "tracker.tv-vault.me": "TVV", -- don't delete automatically
  "tracker.cinemaz.to": "CIN",
  "tracker.pixelhd.me": "PIX"
}

fn = os.path.basename(__file__)
hl = [] #hash list
hld = [] #hash list delete
fl = [] #file list
dlct = 0 #download count
dlsz = 0 #download filesize
hlsz = 0 #hl filesize
tl = [] #create lis for torrents
d = []

# for client in qbt_client.log.log_peers():
#     print(client)


for torrent in qbt_client.torrents_info():
    d.append(tracker_convert(urlparse(torrent.tracker).hostname))
    for i in torrent.trackers:
        for u in str(i.tier):
            if u.isnumeric():
                r = qbt_client.torrents_files(hash=torrent.hash)
                for row in r:
                    fl.append(row.name)
                h = [torrent.hash,torrent.size,torrent.name,tracker_convert(urlparse(torrent.tracker).hostname),1,torrent.ratio,torrent.category,torrent.num_seeds,torrent.seeding_time/86400]
                hl.append(h) if h not in hl else hl
                hlsz += torrent.size
                hld.append(h) if i.msg in ('unregistered torrent','Torrent is not found or it is awaiting moderation','002: Invalid InfoHash, Torrent not found') and h not in hld else hld 
    if (torrent.ratio > 2 and torrent.category == 'archive' and torrent.seeding_time > (60*60*24*30)):
        h = [torrent.hash,torrent.size,torrent.name,tracker_convert(urlparse(torrent.tracker).hostname),3,torrent.ratio,torrent.category,torrent.num_seeds,torrent.seeding_time/86400]
        hld.append(h) if h not in hld else hld
    elif torrent.seeding_time > 7776000:
        h = [torrent.hash,torrent.size,torrent.name,tracker_convert(urlparse(torrent.tracker).hostname),2,torrent.ratio,torrent.category,torrent.num_seeds,torrent.seeding_time/86400]
        hld.append(h) if h not in hld else hld
    elif torrent.ratio > 10: # delete if > 2.0 and in archive or if 30+ days old 
        h = [torrent.hash,torrent.size,torrent.name,tracker_convert(urlparse(torrent.tracker).hostname),4,torrent.ratio,torrent.category,torrent.num_seeds,torrent.seeding_time/86400]
        hld.append(h) if h not in hld else hld

trackct = Counter(d)    #count of items for each tracker   
hld1 = [] 
for rw in hld:
    if rw[4] == 1:
        dm = 'to bad tracker'
    if rw[4] == 2:
        dm = f'to seeding for {round(rw[8])} days' 
    if rw[4] == 3:
        dm = f'to seeding for {round(rw[8])} days and {round(rw[5])} ratio'     
    if rw[4] == 4:
        dm = f'to seeding ratio of {round(rw[5])} '  
    print(trackct[rw[3]])
    if rw[4] == 1 or (rw[4] in (2,3,4) and trackct[rw[3]] > 2):
        print(f'{ts()} - {fn} - {rw[2]} has been deleted due {dm}')
        dlct += 1
        dlsz += rw[1]
        hld1.append(rw[0])

if len(hld1) > 0:
    qbt_client.torrents_delete(torrent_hashes=hld1,delete_files=True)

print(f'{ts()} - {fn} - Scanned a total of {len(hl)} files totalling {sizeof_fmt(hlsz)}')

if len(hld) > 0: 
    print(f'{ts()} - {fn} - Deleted a total of {dlct} file(s) with a total size of {sizeof_fmt(dlsz)}')
else:
    print(f'{ts()} - {fn} - No stale files found to be deleted')
