import time
from zapv2 import ZAPv2
from pprint import pprint
import json

def doScan(target, id):
    try:
        # zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})
        zap = ZAPv2(proxies={'http': 'http://172.19.0.3:8090', 'https': 'http://172.19.0.3:8090'})
                
        #clear previous scans
        zap.spider.remove_all_scans()
        zap.ascan.remove_all_scans()
        zap.core.delete_site_node(target)

        print('Spidering target {}'.format(target))

        # spider scan
        scanID = zap.spider.scan(target) 
        while int(zap.spider.status(scanID)) < 100:
            time.sleep(2)

        # ajax scan
        zap.ajaxSpider.set_option_max_duration(10)
        print(zap.ajaxSpider.option_max_duration)
        scanIDajax = zap.ajaxSpider.scan(target) 
        while zap.ajaxSpider.status == 'running':
            print('Ajax Spider status' + zap.ajaxSpider.status)
            time.sleep(2)
        
        while int(zap.pscan.records_to_scan) > 0:
            print('Records to passive scan : ' + zap.pscan.records_to_scan)
            time.sleep(2)

        print('Passive Scan completed')
        scanners = [40012, 40014, 40018, 40016, 40017, 90018, 40026, 6, 7, 10045, 40009, 
        90019, 90020, 0, 20019, 30001, 30002, 40003, 40008, 50000]
        #zap.ascan.set_option_default_policy('St-High-Th-High')
        #zap.ascan.disable_all_scanners()
        zap.ascan.enable_all_scanners()
        for sc in scanners:
            zap.ascan.set_scanner_alert_threshold(sc, 'High')
            zap.ascan.set_scanner_attack_strength(sc, 'High')
        zap.ascan.set_option_max_rule_duration_in_mins(5)
        zap.ascan.set_option_max_scan_duration_in_mins(120)
        #zap.ascan.enable_scanners(40018,40012)
        scanID = zap.ascan.scan(target)
        while int(zap.ascan.status(scanID)) < 100:
            # Loop until the scanner has finished
            print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
            time.sleep(5)
            aScanID = zap.ascan.scan(target)
        
       
        data = zap.core.htmlreport()
        nameAscan = "pdfs/" + str(id) + "-aScan.html"
        with open(nameAscan, "w") as file:
            file.write(data)
        
        return 0, nameAscan
    except Exception as e:
        pprint(e)
        return 1, str(e)

#doScan("http:localhost", 15)

 #print('Active Scan completed')
        # Print vulnerabilities found by the scanning
        #print('Hosts: {}'.format(', '.join(zap.core.hosts)))
        #print('Alerts: ')
        #pprint(zap.core.alerts(baseurl=target))
        #pprint(zap.core.htmlreport())


        # Print Passive scan results/alerts
        #print('Hosts: {}'.format(', '.join(zap.core.hosts)))
        #print('Alerts: ')
        # pprint(zap.core.alerts())
        # namePscan = str(id) + "-pScan.html"
        # with open("pdfs/" + namePscan, "w") as file:
        #     file.write(zap.core.htmlreport())