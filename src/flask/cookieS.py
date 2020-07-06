from selenium import webdriver
from pyvirtualdisplay import Display
import time
import datetime

def get_cookies(target):
    # display = Display(visible=0, size=(800, 600))
    # display.start()

    #browser=webdriver.Chrome('/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(target)
    while browser.execute_script("return document.readyState;") != "complete":
        continue
    cookiesOLD = browser.get_cookies()
    cookieSW = ['//*[@id="CybotCookiebotDialogBodyLevelButtonAccept"]',
                '//*[@id="qcCmpButtons"]/button[2]',
                '//*[@id="onetrust-accept-btn-handler"]',
                '//*[@id="cookiescript_accept"]' 
    ]       

    # xpathCB = '//*[@id="CybotCookiebotDialogBodyLevelButtonAccept"]'
    # xpathQC = '//*[@id="qcCmpButtons"]/button[2]'
    # xpathOT = '//*[@id="onetrust-accept-btn-handler"]'
    # xpathCS = '//*[@id="cookiescript_accept"]'
    cookiesAdded = []
    for i in cookieSW:
        try:
            browser.find_element_by_xpath(i).click()
            while browser.execute_script("return document.readyState;") != "complete":
                continue
            for j in browser.get_cookies():
                for val in cookiesOLD:
                    #print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val["expiry"])))
                    reg = 1
                    if(j['name'] == val['name']):
                        reg = 0
                        break
                if reg == 1:
                    j["expiry"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(j["expiry"]))
                    cookiesAdded.append(j)
        except Exception as e:
            pass        
    return cookiesOLD, cookiesAdded