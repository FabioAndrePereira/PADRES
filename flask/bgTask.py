import sqlite3 as sql3
import pdfkit
import buildPDF
import time
from flask import Flask, abort, request

#trata de fazer todos os scans assim como construir o pdf
def doAllScans():
    with open("fileGDPR.html", "w") as file:
        file.write("mamamam")
    print("bababababab")
    #time.sleep(60)
    return "hello"
    # content = request.get_json()
    # swName = ''
    # nameCountry = ''
    # swPath = ''
    # dbCon = None
    # try:
    #     dbCon = sql3.connect(PATH_DB)
    #     cursor = dbCon.cursor()   
    #     querySW = 'SELECT description FROM software where id = ?;'
    #     data = cursor.execute(querySW, str(content['sw']))
    #     for i in data:
    #         swName = i[0]

    #     queryCountry = 'SELECT name FROM country where id = ?;'
    #     data = cursor.execute(queryCountry, str(content['country']))
    #     for i in data:
    #         nameCountry = i[0]

    #     queryPATH = 'SELECT pathfiles FROM softwareCountry where softwareID = ? and countryID = ?;'
    #     data = cursor.execute(queryPATH, (str(content['sw']), str(content['country'])))
    #     for i in data:
    #         swPath = i[0]
    # except Exception as e:
    #     print(e)
    #     abort(500, {'message': e})
    # finally:
    #     if dbCon is not None:
    #         try:
    #             dbCon.close()
    #             #app.logger.info("dbcon closed {}".format(dbCon))
    #         except Exception as e:
    #             #app.logger.error("Error closing con {}".format(e))
    #             print("Error closing con {}".format(e))

    # # generate pdf for gdpr and security report
    # try:
    #     htmlGDPR, timestamp = buildPDF.buildPDF(content, swName, nameCountry, content['country'], content['sw'])     
    #     # CALL ZAP and others with timestamp
    #     time.sleep(60*3)
    #     # generate final pdf 
    #     with open("fileGDPR-"+ timestamp + ".html", "w") as file:
    #         file.write(htmlGDPR)
    #     # pdfkit.from_file(["fileGDPR-"+ timestamp + ".html", 'repPassive'+timestamp+'.html', 'repActive'+timestamp+'.html'], 'report-' +timestamp+ '.pdf')  
    #     pdfkit.from_file("fileGDPR-"+ timestamp + ".html", 'report-' +timestamp+ '.pdf')
    #     # falta inserir na db
    #     return 200
    # except Exception as e:
    #     print(e)
    #     return 500
    #     #abort(500, {'message': e})