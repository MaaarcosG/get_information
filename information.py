import platform as pl
import socket
import sys 
import psutil
import os

def get_size(bytes, suffix="B"):
    pass

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

print("="*40, "System Information", "="*40)
for i in perfil_information:
    if hasattr(pl, i):
        print('[+] %s: %s' % (i, getattr(pl,i)()))

print ("Number of CPUs: " +str(psutil.cpu_count()))
print ("Number of Physical CPUs: " +str(psutil.cpu_count(logical=False)))

def getMachine_addr():
    """ Find OS and run appropriate read mobo serial num command"""
    os_type = sys.platform.lower()
 
    if "win" in os_type:
        command = "wmic bios get serialnumber"
 
    elif "linux" in os_type:
        command = "hal-get-property --udi /org/freedesktop/"  \
        "Hal/devices/computer --key system.hardware.uuid"
 
    elif "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
    return os.popen(command).read().replace("\n", "").replace("  ", "").replace(" ", "")
 
print("Your motherboard", getMachine_addr())