import platform as pl
import socket
import sys 
import psutil

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