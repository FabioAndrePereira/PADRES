import time
from zapv2 import ZAPv2
from pprint import pprint
import json
# The URL of the application to be tested
target = 'https://public-firing-range.appspot.com'
# Change to match the API key set in ZAP, or use None if the API key is disabled

# By default ZAP API client will connect to port 8080
#zap = ZAPv2(apikey=apiKey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# print('Spidering target {}'.format(target))
# # The scan returns a scan id to support concurrent scanning
# scanID = zap.spider.scan(target) # spider scan
# print(scanID)
# while int(zap.spider.status(scanID)) < 100:
#     print('Ajax status ' + zap.spider.status(scanID))
#     time.sleep(1)

# print('Spider has completed!')

# # Prints the URLs the spider has crawled
# print('\n'.join(map(str, zap.spider.results(scanID))))
# fName = scanID + ".json"
# jsonRes = json.dumps('\n'.join(zap.spider.results(scanID)))
# with open(fName, 'w') as file:
#     file.write(jsonRes)
# #print('\n'.join(map(str, zap.ajaxSpider.results(scanID))))
# # If required post process the spider results

# print('Active Scanning target {}'.format(target))
# scanID = zap.ascan.scan(target)
# print(zap.ascan.scanners)
# while int(zap.ascan.status(scanID)) < 100:
#     # Loop until the scanner has finished
#     print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
#     print('Scan progress %: {}'.format(zap.ascan.scan_progress(scanID)))
#     time.sleep(5)

# print('Active Scan completed')
# # Print vulnerabilities found by the scanning
# print('Hosts: {}'.format(', '.join(zap.core.hosts)))
# print('Alerts: ')
# pprint(zap.core.alerts(baseurl=target))

def doScan(target):
    # The scan returns a scan id to support concurrent scanning
    # print('Spidering target {}'.format(target))
    # contextName = target + "/*"
    # spider scan
    scanID = zap.spider.scan(target) 
    while int(zap.spider.status(scanID)) < 100:
        print('Ajax status ' + zap.spider.status(scanID))
        time.sleep(1)
    # # spider ajax scan
    # timeout = time.time() + 60*2
    # scanIDajax = zap.ajaxSpider.scan(target) 
    # while zap.ajaxSpider.status == 'running':
    #     if time.time() > timeout:
    #         break
    #     print('Ajax Spider status' + zap.ajaxSpider.status)
    #     time.sleep(2)
    
    # while int(zap.pscan.records_to_scan) > 0:
    #     # Loop until the passive scan has finished
    #     print('Records to passive scan : ' + zap.pscan.records_to_scan)
    #     time.sleep(2)

    # print('Passive Scan completed')

    # # Print Passive scan results/alerts
    # print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    # print('Alerts: ')
    # pprint(zap.core.alerts())
    # with open("repPassive.html", "w") as file:
    #     file.write(zap.core.htmlreport())
    

    scanID = zap.ascan.scan(target)
    while int(zap.ascan.status(scanID)) < 100:
        # Loop until the scanner has finished
        print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(5)
        aScanID = zap.ascan.scan(target)
    
    print('Active Scan completed')
    # Print vulnerabilities found by the scanning
    print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    print('Alerts: ')
    pprint(zap.core.alerts(baseurl=target))

    with open("repActive.html", "w") as file:
        file.write(zap.core.htmlreport())
    
    #return html

doScan(target)