import subprocess
import os

def bluetooth_ping(mac):
    out = subprocess.Popen(['sudo l2ping -c 1 ' + mac],
       shell=True,
       stdout=subprocess.PIPE,
       stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    std_str = str(stdout)
                           
    if "down" in std_str:
        return [False]
    elif "from" in std_str:
        os.system("sudo l2ping -c 2 " + mac + " > /dev/null 2>&1 &")
        get_rssi(mac)
        return [True, get_rssi(mac)]
    return [False]
    
    
def get_rssi(mac):
    out = subprocess.Popen(['hcitool rssi ' + mac],
       shell=True,
       stdout=subprocess.PIPE,
       stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    std_str = str(stdout)
    try:
        return int((std_str.split(' ')[-1]).replace("\\n'", ""))
    except:
        return 0
   
