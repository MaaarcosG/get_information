import platform
import cpuinfo
import psutil
import os
import sys

def computer_data():
    perfil_information = ['architecture', 'machine', 'release', 'system', 'version', 'node', 'platform', 'processor']
    print(' ')
    print('='*40, 'System Information', '='*40)
    # recorremos lista para obtener los datos
    for data in perfil_information:
        if hasattr(platform, data):
            print('[+] %s: %s' % (data, getattr(platform,data)()))

def getSeialNumber():
    # serial number HDD
    os_type = sys.platform.lower()
    if 'darwin' in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
        print('[+] Serial Number: %s' % os.popen(command).read().split()[-1])
    elif 'win' in os_type:
        command = "wmic bios get serialnumber"
        print('[+] Serial Number: %s' % os.popen(command).read().split()[-1])
    elif 'linux' in os_type:
        serialnumber = "hdparm -I /dev/sda | grep 'Serial Number'"
        modelnumber = "hdparm -I /dev/sda | grep 'Model'"

        print('[+] Serial Number: %s' % os.popen(serialnumber).read().split()[-1])
        print('[+] Model Number: %s' % os.popen(modelnumber).read().split()[-2])

def number_CPU():
    name_processor = cpuinfo.get_cpu_info()['brand_raw']
    numberCPU = str(psutil.cpu_count(logical=True))
    physical_cpu = str(psutil.cpu_count(logical=False))
    # sacaremos la frecuencia del procesador
    frecuency = psutil.cpu_freq()

    print("="*40, "CPU Information", "="*40)
    print('[+] Processor: %s' % name_processor)
    print('[+] Number of CPUs: %s' % numberCPU)
    print('[+] Number of Physical CPUs: %s' % physical_cpu)
    print(f'[+] Max Frequency: {frecuency.max:.2f} Mhz')
    print(f'[+] Min Frequency: {frecuency.min:.2f} Mhz')
    print(f'[+] Current Frequency: {frecuency.current:.2f} Mhz \n')

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"[+] CPU Usage of Core {i}: {percentage}%")
        print(f"[+] Total CPU Usage: {psutil.cpu_percent()}%")

def memory_data():
    disk_partitions = psutil.disk_partitions()
    print('='*40, 'Memory Information', '='*40)
    for partition in disk_partitions:
        print("[+] Partition Device: %s" % partition.device)
        print("[+] File System: %s" % partition.fstype)
        print("[+] Mountpoint: %s" % partition.mountpoint)

        disk_usage = psutil.disk_usage(partition.mountpoint)
        print("[+] Total Disk Space : %d GB" % gb_bytes(disk_usage.total))
        print("[+] Free Disk Space %d GB" % gb_bytes(disk_usage.free))
        print("[+] Used Disk Space %d GB" % gb_bytes(disk_usage.used))
        print("[+] Percentage Used %d %s \n" % (disk_usage.percent, '%'))

def gb_bytes(bytes):
    gb = bytes/(1024*1024*1024)
    return round(gb,2)

if __name__ == '__main__':
    '''
    computer_data()
    getSeialNumber()
    number_CPU()
    '''
    memory_data()