#!/usr/bin/python3
import os
from functions import ts, sizeof_fmt, qb

d = '/mnt/btrfs/downloads/torrent/'
sd = 0
ds = 0
tl = []
dl = []
z = []
fn = os.path.basename(__file__)
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
for torrent in qb.torrents_info():
    for i in torrent.trackers:
        r = qb.torrents_files(hash=torrent.hash)
        for row in r:
            ta = torrent.save_path+'/'+row.name
            tl.append(ta) if ta not in tl else ta

if len(tl) < 2:
    print(f'{ts()} - No torrents found, exiting script.')
    quit()

# Delete files not in list loaded from QBT
for sdir in subdirs:
    for r, d, f in os.walk(sdir):
        for file in f:
            a = os.path.join(r, file)
            if os.path.isfile(os.path.join(r, file)) and os.path.join(r, file) not in tl:
                dfn = os.path.join(r, file)
                fs = os.stat(dfn).st_size
                sd += 1
                ds += fs
                dl.append(dfn)
                print(f'{ts()} - {fn} - Deleted - {dfn} - {sizeof_fmt(fs)}')

# Delete files from list
for file in dl:
    os.remove(file)

if sd==0:
    print(f'{ts()} - {fn} - No leftover files found.')
else:
    print(f'{ts()} - {fn} - Deleted a total of {sd} leftover file(s) totaling {sizeof_fmt(ds)} ')