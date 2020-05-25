import nmap
import subprocess   
def nmapScan(target, nameXML, nameHTML):
    nmScan = nmap.PortScanner()
    nmScan.scan(hosts=target,  arguments='-A --script=vulners.nse')
    out = nmScan.get_nmap_last_output()
    with open(nameXML, 'w') as file:
            file.write(out)
    process = subprocess.call(['xsltproc', nameXML, '-o', nameHTML])
