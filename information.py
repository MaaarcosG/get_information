import platform as pl
import socket
import sys 
import psutil
import os
import fcntl
import struct

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

    if os.geteuid() >  0:
        print("ERROR: Must be root to use")
        sys.exit(1)

    with open(partition.device, "rb") as fd:
        hd_driveid_format_str = "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"
        HDIO_GET_IDENTITY = 0x030d
        sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)

        assert sizeof_hd_driveid == 512 
        buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid)
        fields = struct.unpack(hd_driveid_format_str, buf)
        serial_no = fields[10].strip()
        model = fields[15].strip()
        print("Hard Disk Model: %s" % model)
        print("Serial Number: %s" % serial_no)

