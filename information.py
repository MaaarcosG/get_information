import platform
import cpuinfo
import psutil
import os
import sys
import struct
import fcntl


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
        '''
        serialnumber = "hdparm -I /dev/sda | grep 'Serial Number'"
        modelnumber = "hdparm -I /dev/sda | grep 'Model'"

        print('[+] Serial Number: %s' % os.popen(serialnumber).read().split()[-1])
        print('[+] Model Number: %s' % os.popen(modelnumber).read().split()[-2])
        '''
        with open('/dev/sda', 'rb') as fd:
            hd_driveid_format_str = "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"

            HDIO_GET_IDENTITY = 0x030d 
            sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)

            assert sizeof_hd_driveid == 512
            buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid) 
            fields = struct.unpack(hd_driveid_format_str, buf)
            serial_no = fields[10].strip()
            model = fields[15].strip()
            print("[+] Hard Disk Model: %s" % model)
            print("[+] Serial Number: %s" % serial_no)

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
    print(f'[+] Max Frequency: {ghz_mhz(frecuency.max):.2f} Ghz')
    print(f'[+] Min Frequency: {ghz_mhz(frecuency.min):.2f} Ghz')
    print(f'[+] Current Frequency: {ghz_mhz(frecuency.current):.2f} Ghz \n')

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

def ghz_mhz(data):
    ghz = data/1000
    return ghz

if __name__ == '__main__':
    computer_data()
    getSeialNumber()
    number_CPU()
    memory_data()






