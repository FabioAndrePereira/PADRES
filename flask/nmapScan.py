import nmap
import subprocess   
def nmapScan(target):
    nmScan = nmap.PortScanner()
    nmScan.scan(hosts="127.0.0.1",  arguments='-sV --script=nmap-vulners/vulners.nse')
    return nmScan.get_nmap_last_output()
   #  with open("scan.xml", "w") as file:
   #     file.write(nmScan.get_nmap_last_output())
   #  process = subprocess.call(['xsltproc', 'scan.xml', '-o', 'scan.html'])


