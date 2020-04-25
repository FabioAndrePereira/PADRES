import time
from zapv2 import ZAPv2
from pprint import pprint
import json
# The URL of the application to be tested
#target = 'https://public-firing-range.appspot.com'
# Change to match the API key set in ZAP, or use None if the API key is disabled

# By default ZAP API client will connect to port 8080
#zap = ZAPv2(apikey=apiKey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
#zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

def doScan(target, id):
    zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})
    # The scan returns a scan id to support concurrent scanning
    target = 'https://public-firing-range.appspot.com'
    print('Spidering target {}'.format(target))
    # contextName = target + "/*"
    # spider scan
    scanID = zap.spider.scan(target) 
    while int(zap.spider.status(scanID)) < 100:
        #print('Ajax status ' + zap.spider.status(scanID))
        time.sleep(2)
    # # spider ajax scan
    zap.ajaxSpider.set_option_max_duration(2)
    print(zap.ajaxSpider.option_max_duration)
    scanIDajax = zap.ajaxSpider.scan(target) 
    while zap.ajaxSpider.status == 'running':
        print('Ajax Spider status' + zap.ajaxSpider.status)
        time.sleep(2)
    
    while int(zap.pscan.records_to_scan) > 0:
        print('Records to passive scan : ' + zap.pscan.records_to_scan)
        time.sleep(2)

    print('Passive Scan completed')

    # Print Passive scan results/alerts
    #print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    #print('Alerts: ')
    # pprint(zap.core.alerts())
    # namePscan = str(id) + "-pScan.html"
    # with open("pdfs/" + namePscan, "w") as file:
    #     file.write(zap.core.htmlreport())
    

    scanID = zap.ascan.scan(target)
    while int(zap.ascan.status(scanID)) < 100:
        # Loop until the scanner has finished
        print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(5)
        aScanID = zap.ascan.scan(target)
    
    #print('Active Scan completed')
    # Print vulnerabilities found by the scanning
    #print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    #print('Alerts: ')
   # pprint(zap.core.alerts(baseurl=target))
    nameAscan = str(id) + "-aScan.html"
    with open("pdfs/" + nameAscan, "w") as file:
        file.write(zap.core.htmlreport())
    
    return  nameAscan

#doScan("https://public-firing-range.appspot.com", 15)