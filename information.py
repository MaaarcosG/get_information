import platform as pl
import socket
import sys 
import psutil
import os

def get_size(bytes, suffix="B"):
    pass

def bytes_to_gbytes(bytes):
    gb = bytes/(1024*1024*1024)
    gb = round(gb,2)
    return gb

# DATOS DE LA COMPUTADORA 

perfil_information = [
    'architecture',
    'machine',
    'release',
    'system',
    'version',
    'node',
    'platform',
    'processor'
]
print(' ')
print("="*40, "System Information", "="*40)
for i in perfil_information:
    if hasattr(pl, i):
        print('[+] %s: %s' % (i, getattr(pl,i)()))

print(' ')
print("="*40, "CPU Information", "="*40)
print ("[+] Number of CPUs: %s " % str(psutil.cpu_count()))
print ("[+] Number of Physical CPUs: %s " % str(psutil.cpu_count(logical=False)))

with open("/proc/cpuinfo", "r") as f:
    file_info = f.readlines()

cpuinfo = [x.strip().split(":")[1] for x in file_info if "model name" in x]
for index, item in enumerate(cpuinfo):
    print("[+] Processor: %s: %s" % (str(index), item))


print(' ')
print("="*40, "Disk Information", "="*40)
disk_partitions = psutil.disk_partitions()
for partition in disk_partitions:
    print("[+] Partition Device: %s" % partition.device)
    print("[+] File System: %s" % partition.fstype)
    print("[+] Mountpoint: %s " % partition.mountpoint)

    print('Disk Usage')
    disk_usage = psutil.disk_usage(partition.mountpoint)
    print("[+] Total Disk Space : %d GB" % bytes_to_gbytes(disk_usage.total))
    print("[+] Free Disk Space %d GB" % bytes_to_gbytes(disk_usage.free))
    print("[+] Used Disk Space %d GB" % bytes_to_gbytes(disk_usage.used))
    print("[+] Percentage Used %d %s" % (disk_usage.percent, '%'))

disk_rw = psutil.disk_io_counters()
print(f"[+] Total Read since boot : {bytes_to_gbytes(disk_rw.read_bytes)} GB")
print(f"[+] Total Write sice boot : {bytes_to_gbytes(disk_rw.write_bytes)} GB")

