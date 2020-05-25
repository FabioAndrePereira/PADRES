#flask
import sqlite3 as sql3
from flask import Flask, abort, request, send_file
from flask_cors import CORS
#aux lib
import conDB as conDB
import nmapScan
import wp
import zap
import jsonParser
import buildPDF
#main lib
import os
import subprocess 
import atexit
#ext lib
import redis
import pdfkit
from rq import Worker, Queue, Connection
from redis import Redis
from rq.job import Job
from rq.registry import FailedJobRegistry, ScheduledJobRegistry
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)


failed_registry = FailedJobRegistry(queue=q)
for job_id in failed_registry.get_job_ids():
    app.logger.error("fal del-> " + str(job_id))
    failed_registry.remove(job_id, delete_job=True)

# sch_registry = ScheduledJobRegistry(queue=q)
# for job_id in sch_registry.get_job_ids():
#     app.logger.error("sch del-> " + str(job_id))
#     sch_registry.remove(job_id, delete_job=True)

def job_function():
    con = conDB.newCon()
    data = conDB.getPDFs(con).fetchall()
    # ter em conta time out to job result
    # ver se status é 0 o u 1 antes de chamar result
    for i in data:
        if i[6] == 0: # status for 0 faz call para obter resultado do job 
            job = Job.fetch(i[5],connection=redis_conn)
            #ver se ja cabou ou n
            if job.get_status() == "finished":
                pdfName = job.result[1] # full path
                with open(pdfName, 'rb') as input_file:
                    ablob = input_file.read()
                    conDB.insertPDF(i[0], pdfBLOB=ablob)
            elif job.get_status() == "failed":
                conDB.insertPDF(i[0], status=-1)

        else:
            continue

sched = BackgroundScheduler(daemon=True)
sched.add_job(job_function,'interval',seconds=60)
sched.start()

#https://stackoverflow.com/questions/21214270/scheduling-a-function-to-run-every-hour-on-flask
atexit.register(lambda: sched.shutdown(wait=False))
#PATH_DB = 'gdpr.db'

@app.cli.command("run_worker")
def runWorker():
    listen = ['default']
    #redis_url = 'redis://localhost:6379'
    redis_url = 'redis://redis:6379/0'

    conn = redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker(listen)
        worker.work()

@app.route('/', methods=['GET'])
def entry():
    return "HELLO"


@app.route('/rules/<cID>', methods=['GET'])
def rules(cID):
    dbCon = None
    try:
        dbCon = conDB.newCon()
        cursor = dbCon.cursor()
        queryRulesCountry = 'SELECT id as rID, definition as rDefinition FROM  rule ' \
                            'INNER JOIN ruleCountry rC ON rule.id = rC.ruleID ' \
                            'WHERE rC.countryID = ?'
        data = cursor.execute(queryRulesCountry,  cID)
        response = app.response_class(
            response=jsonParser.rulesJSON(data.fetchall()),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        abort(500, {'message': e})
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
                app.logger.info("dbcon closed {}".format(dbCon))
            except Exception as e:
                app.logger.error("Error closing con {}".format(e))

# get principles for each principle
@app.route('/principles/<phID>', methods=['GET'])
def principles(phID):
    dbCon = None
    try:
        dbCon = conDB.newCon()
        data = conDB.getPrinciples(dbCon, phID)
        response = app.response_class(
            response=jsonParser.principlesJSON(data.fetchall()),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        abort(500, {'message': e})
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
                app.logger.info("dbcon closed {}".format(dbCon))
            except Exception as e:
                app.logger.error("Error closing con {}".format(e))

@app.route('/sw/<cID>', methods=['GET'])
def sw(cID):
    dbCon = None
    try:
        dbCon = conDB.newCon()
        cursor = dbCon.cursor()
        queryPrinciples = 'SELECT * FROM software;'
        data = cursor.execute(queryPrinciples)
        if int(cID) > 0:
            queryPrinciples = 'SELECT s.id, s.description FROM software s ' \
                              'INNER JOIN softwareCountry sC on sC.softwareID = s.id ' \
                              'WHERE sC.countryID = ?'
            data = cursor.execute(queryPrinciples, cID)

        response = app.response_class(
            response=jsonParser.swJSON(data.fetchall()),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        abort(500, {'message': e})
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
                app.logger.info("dbcon closed {}".format(dbCon))
            except Exception as e:
                app.logger.error("Error closing con {}".format(e))

@app.route('/principleH', methods=['GET'])
def principleH():
    dbCon = None
    try:
        dbCon = conDB.newCon()
        data = conDB.getPrincipleHeader(dbCon)
        response = app.response_class(
            response=jsonParser.phJSON(data.fetchall()),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        abort(500, {'message': e})
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
                app.logger.info("dbcon closed {}".format(dbCon))
            except Exception as e:
                app.logger.error("Error closing con {}".format(e))

@app.route('/country', methods=['GET'])
def country():
    dbCon = None
    try:
        dbCon = conDB.newCon()
        cursor = dbCon.cursor()
        queryCountry = 'SELECT * from country;'
        data = cursor.execute(queryCountry)
        response = app.response_class(
            response=jsonParser.countryJSON(data.fetchall()),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        abort(500, {'message': e})
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
                app.logger.info("dbcon closed {}".format(dbCon))
            except Exception as e:
                app.logger.error("Error closing con {}".format(e))


@app.route('/postDataForm', methods=['POST'])
def postDataForm():
    content = request.get_json()
    swName = ''
    nameCountry = ''
    swPath = ''
    dbCon = None
    try:
        dbCon = conDB.newCon()
        cursor = dbCon.cursor()   
        querySW = 'SELECT description FROM software where id = ?;'
        data = cursor.execute(querySW, str(content['sw']))
        for i in data:
            swName = i[0]

        queryCountry = 'SELECT name FROM country where id = ?;'
        data = cursor.execute(queryCountry, str(content['country']))
        for i in data:
            nameCountry = i[0]

        # queryPATH = 'SELECT pathfiles FROM softwareCountry where softwareID = ? and countryID = ?;'
        # data = cursor.execute(queryPATH, (str(content['sw']), str(content['country'])))
        # for i in data:
        #     swPath = i[0]
    except Exception as e:
        abort(500, {'message': e})
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
                app.logger.info("dbcon closed {}".format(dbCon))
            except Exception as e:
                app.logger.error("Error closing con {}".format(e))
                print("Error closing con {}".format(e))

    # build html for gdpr
    htmlGDPR, timestamp = buildPDF.buildPDF(content, swName, nameCountry) 
    try:    
        # start security scans in bg
        con = conDB.newCon()
        idPDF = conDB.createPDFentry(con, str(content['country']), str(content['sw']), timestamp) # insere e retorna o id da inserção
        app.logger.info("start job")
        job = q.enqueue(doAllScans, args=(htmlGDPR, timestamp, idPDF, content["doNMAP"], 
                        content["doZAP"] ,str(content["ZAPurl"])), job_timeout=3600*5)
        jobID = str(job.get_id())
        conDB.insertJobID(con, jobID, idPDF)
        response = app.response_class(
            status=202
        )
        return response
    except Exception as e:
        print(e)
        abort(500, {'message': e})
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
                app.logger.info("dbcon closed {}".format(dbCon))
            except Exception as e:
                app.logger.error("Error closing con {}".format(e))
                print("Error closing con {}".format(e))

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key,connection=redis_conn)
    return str(job.get_status()), 200

@app.route("/allJobsQueue", methods=['GET'])
def get_allJQ():
    sch_registry = ScheduledJobRegistry(queue=q)
    return str(sch_registry)

@app.route("/allJobsFailed", methods=['GET'])
def get_allJF():
    failed_registry = FailedJobRegistry(queue=q)        
    return str(failed_registry)
    
@app.route('/getPDFs', methods=['GET'])
def getPDFs():
    con = None
    try:
        con = conDB.newCon()
        data = conDB.getPDFs(con)
        response = app.response_class(
            response=jsonParser.pdfsJSON(data.fetchall()),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        print(e)
        abort(500, {'message': e})
    finally:
        try: 
            con.close()
            app.logger.info("dbcon closed {}".format(con))
        except Exception as e:
            app.logger.error("Error closing con {}".format(e))

@app.route('/returnPDF/<pdfID>')
def returnPDF(pdfID):
    reportName = "/usr/src/app/pdfs/report-" + str(pdfID) + ".pdf"
    if not os.path.exists(reportName):  
        #app.logger.error("buildpdf")
        con = conDB.newCon()
        data = conDB.getSelectedPDF(con, pdfID).fetchone()
        with open(reportName, 'wb') as output_file:
            output_file.write(data)
    try:
        #app.logger.error(os.path.exists(reportName))
        return send_file(reportName, attachment_filename='report-' + str(pdfID) + '.pdf')
    except Exception as e:
	    return str(e)
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

def doAllScans(htmlGDPR, timestamp, idPDF, doNMAP, doZAP, zapURL):
    if doZAP:
        html ="""
            <!DOCTYPE html>
            <html>
                <head>
                    <style>
                        table, th{
                            border: 1px solid black;
                        }
                        th, td {
                            padding: 10px;
                        }
                        th{
                            background:#6CA4EC;
                        }
                    </style>
                </head>
                <body>   
            """
        # adicionar coookies
        import cookieS
        cookieOld, cookieN = cookieS.get_cookies(zapURL)
        if len(cookieOld) != 0:
            print("addind cookies")
            html += """<h3><font color=\"black\"> Cookies before consent </font></h3>"""
            html += """
            <table style="width:100%">
                <tr>
                <th>Name</th>
                <th>Domain</th>
                <th>Expiration</th>
                <th>httpOnly</th>
                <th>Value</th>
                </tr>
            """
            for c in cookieOld:
                html += """
                    <tr>
                        <td>""" + str(c['name'])     + """</td>
                        <td>""" + str(c['domain'])   + """</td>
                        <td>""" + str(c['expiry'])   + """</td>
                        <td>""" + str(c['httpOnly']) + """</td>
                        <td>""" + str(c['value'])    + """</td>
                    </tr>
                    """
            html += "</table>"
        else:
            html += """<h3><font color=\"black\"> No Cookies Retrived </font></h3>"""
        if len(cookieN) != 0:
            html += """<h3><font color=\"black\"> Cookies added after consent </font></h3>"""
            html += """
            <table style="width:100%">
                <tr>
                <th>Name</th>
                <th>Domain</th>
                <th>Expiration</th>
                <th>httpOnly</th>
                <th>Value</th>
                </tr>
            """
            for c in cookieN:
                html += """
                <tr>
                    <td>""" + str(c['name'])     + """</td>
                    <td>""" + str(c['domain'])   + """</td>
                    <td>""" + str(c['expiry'])   + """</td>
                    <td>""" + str(c['httpOnly']) + """</td>
                    <td>""" + str(c['value'])    + """</td>
                </tr>
                """
            html += "</table>" 
        elif len(cookieOld) != 0:
            html += """<h3><font color=\"black\"> Was not possible to retrive cookies after consent </font></h3>"""
        html += """
                </body>
            </html>
        """ 
        nameCookie_Scan = "pdfs/" + str(idPDF) + "-cookieScan.html"
        with open(nameCookie_Scan, "w") as file:
            file.write(html)

    if doNMAP:
        nmapIP = zapURL.split('//')[1].split('/')[0]
        if ':' in nmapIP:
            nmapIP = nmapIP.split(':')[0]
        app.logger.info("NMAP")
        app.logger.error(nmapIP)
        nmapScan.nmapScan(nmapIP, 'pdfs/' + str(idPDF) + '.xml', 'pdfs/' + str(idPDF) + '.html')
        # nameXML = "pdfs/" + str(idPDF) + ".xml"
        nameHTML = "pdfs/" + str(idPDF) + ".html"
        # with open("pdfs/" + str(idPDF) + ".xml", "w") as file:
        #     file.write(out)
        # process = subprocess.call(['xsltproc', nameXML, '-o', nameHTML ])

    
    # perform zap scan and wapiti
    nameAscan = ""
    if doZAP:
        app.logger.info("ZAP")
        htmlaScan =  zap.doScan(zapURL, idPDF)
        if htmlaScan[0] == 1: # houve erro a produzir report
            html ="""
                <!DOCTYPE html>
                <html>
                    <body>
                        <h3>ERROR performing OWASP ZAP SCAN</h3>
                        <h3>ERROR: """ + htmlaScan[1] + """ </h3>
                    </body>
                </html>
            """   
            nameAscan = "pdfs/" + str(idPDF) + "-aScan.html"
            with open(nameAscan, "w") as file:
                file.write(html)
        else: # nao falhou
            nameAscan = htmlaScan[1]
        # do wapiti
        app.logger.info("WAPITI")
        nameWPscan = "pdfs/" + str(idPDF) + "-WPscan.html"
        codeWP = wp.doWapiti(nameWPscan, zapURL)

    
    nameHTMLGDPR = "pdfs/" + str(idPDF) + "-gdpr.html"
    with open(nameHTMLGDPR, "w") as file:
        file.write(htmlGDPR)
    
    # build final pdf
    app.logger.info("FINAl PDF")
    reportName = "/usr/src/app/pdfs/report-" + str(idPDF) + ".pdf"
    if doNMAP and doZAP:
        pdfkit.from_file([nameHTMLGDPR, nameCookie_Scan, nameHTML, nameAscan, nameWPscan], reportName) 
    elif doZAP and (codeWP == 1):
        pdfkit.from_file([nameHTMLGDPR, nameCookie_Scan, nameAscan, nameWPscan], reportName)
    elif doNMAP:
        pdfkit.from_file([nameHTMLGDPR, nameHTML], reportName)
    else:
        #app.logger.error("build pdf")
        pdfkit.from_file([nameHTMLGDPR], reportName)
    

    return 1, reportName
  
   
    
