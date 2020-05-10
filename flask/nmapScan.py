import nmap
import subprocess   
def nmapScan(target):
    nmScan = nmap.PortScanner()
    nmScan.scan(hosts=target,  arguments='-A --script=nmap-vulners/vulners.nse')
    return nmScan.get_nmap_last_output()
