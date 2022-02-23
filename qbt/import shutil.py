import shutil
import os


src = '/mnt/btrfs/downloads/.snapshots/31/snapshot/torrent/archive/Reservation.Dogs.S01E02.NDN.Clinic.1080p.HULU.WEB-DL.DDP5.1.H.264-FLUX.mkv'
dst  = '/mnt/btrfs/downloads/torrent/archive/Reservation.Dogs.S01E02.NDN.Clinic.1080p.HULU.WEB-DL.DDP5.1.H.264-FLUX.mkv'
shutil.copyfile(src, dst)