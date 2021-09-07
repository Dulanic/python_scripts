#!/usr/bin/python3
import sys, os
from functions import ts, sizeof_fmt, qbt_client

pathroot = '/mnt/btrfs/downloads/torrent/'
sd = 0
ds = 0
tl = []
fn = os.path.basename(__file__)

# Load list of all files in qbt
for torrent in qbt_client.torrents_info():
    for i in torrent.trackers:
        r = qbt_client.torrents_files(hash=torrent.hash)
        for row in r:
            ta = torrent.save_path+row.name
            tl.append(ta) if ta not in tl else ta

if len(tl) < 2:
    print(f'{ts()} - No torrents found, exiting script.')
    quit()

# Delete files not in list loaded from QBT
for sdir in ['sonarr','radarr','radarr4k','archive']:
    for r, d, f in os.walk(pathroot+sdir):
        for file in f:
            a = os.path.join(r, file)
            if os.path.isfile(os.path.join(r, file)) and os.path.join(r, file) not in tl:
                fn = os.path.join(r, file)
                fs = os.stat(fn).st_size
                sd += 1
                ds += fs
                os.remove(fn)
                print(f'{ts()} - Deleted - {fn} - {sizeof_fmt(fs)}')

if sd==0:
    print(f'{ts()} - {fn} - No leftover files found.')
else:
    print(f'{ts()} - {fn} - Deleted a total of {sd} leftover file(s) totaling {sizeof_fmt(ds)} ')