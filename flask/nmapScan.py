import nmap
import subprocess

def nmapScan():
    nmScan = nmap.PortScanner()
    nmScan.scan(hosts="scanme.nmap.org",  arguments='-sV --script=nmap-vulners/vulners.nse')
    with open("scan.xml", "w") as file:
       file.write(nmScan.get_nmap_last_output())
    process = subprocess.call(['xsltproc', 'scan.xml', '-o', 'scan.html'])


