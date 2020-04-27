import sqlite3 as sql3
from flask import Flask, abort, request, send_file
from flask_cors import CORS
import jsonParser as jsonParser
import pdfGenerator as pdfGen
import conDB as conDB
import buildPDF
import pdfkit
import redis
import nmapScan
import subprocess 
import zap
#from bgTask import doAllScans
from rq import Worker, Queue, Connection
from redis import Redis
from rq.job import Job
from pdfrw import PdfReader, PdfWriter
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)

PATH_DB = 'gdpr.db'

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
        dbCon = sql3.connect(PATH_DB)
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
        dbCon = sql3.connect(PATH_DB)
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
        dbCon = sql3.connect(PATH_DB)
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
        dbCon = sql3.connect(PATH_DB)
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
        dbCon = sql3.connect(PATH_DB)
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
        dbCon = sql3.connect(PATH_DB)
        cursor = dbCon.cursor()   
        querySW = 'SELECT description FROM software where id = ?;'
        data = cursor.execute(querySW, str(content['sw']))
        for i in data:
            swName = i[0]

        queryCountry = 'SELECT name FROM country where id = ?;'
        data = cursor.execute(queryCountry, str(content['country']))
        for i in data:
            nameCountry = i[0]

        queryPATH = 'SELECT pathfiles FROM softwareCountry where softwareID = ? and countryID = ?;'
        data = cursor.execute(queryPATH, (str(content['sw']), str(content['country'])))
        for i in data:
            swPath = i[0]
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
        app.logger.error("aqui crl 0")
        print("START JOB")
        app.logger.error("aqui crl 1")
        job = q.enqueue(doAllScans, args=("127.0.0.1", htmlGDPR, timestamp, idPDF), job_timeout=3600)
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
    return str(job.result), 200
    

@app.route('/getPDFs', methods=['GET'])
def getPDFs():
    con = None
    try:
        con = conDB.newCon()
        data = conDB.getPDFs(con).fetchall()
        # ter em conta time out to job result
        # ver se status é 0 o u 1 antes de chamar result
        folder = os.listdir("pdfs/")
        app.logger.error(folder)
        # for i in data:
        #     if i[6] == 0: # status for 0 faz call para obter resultado do job 
        #         job = Job.fetch(i[5],connection=redis_conn)
        #         #ver se ja cabou ou n
        #         if job.get_status() == "finished":
        #             pdf = job.result[1]
        #             #app.logger.error
        #             #PdfWriter(job[2], trailer=pdf).write()
        #             #conDB.insertPDF(i[0], pdf)
        #     else:
        #         continue
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

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file('pdfs/report-56.pdf', attachment_filename='report-56.pdf')
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

def doAllScans(ipTarget, htmlGDPR, timestamp, idPDF):
   # perform nmap scan
#    app.logger.error("NMAP")
    out = nmapScan.nmapScan(ipTarget)
    nameXML = "pdfs/" + str(idPDF) + ".xml"
    nameHTML = "pdfs/" + str(idPDF) + ".html"
    with open("pdfs/" + str(idPDF) + ".xml", "w") as file:
        file.write(out)

    process = subprocess.call(['xsltproc', nameXML, '-o', nameHTML ])
    #app.logger.error("ZAP")
    # perform zap scan
    htmlaScan =  zap.doScan(ipTarget, idPDF)
    # build final pdf
    nameHTMLGDPR = "pdfs/" + str(idPDF) + "-gdpr.html"
    with open(nameHTMLGDPR, "w") as file:
        file.write(htmlGDPR)

    reportName = "/usr/src/app/pdfs/report-" + str(idPDF) + ".pdf"
    
    pdfkit.from_file([nameHTMLGDPR, nameHTML, htmlaScan], reportName)  
    #x = pdfkit.from_file([nameHTMLGDPR, nameHTML], reportName)  
    
    pdf = PdfReader(reportName)
    return 1, pdf, reportName
    #return x
   #pdf = pdfkit.from_file(nameHTMLGDPR, False)  

   
  # val = conDB.insertPDF(idPDF, reportName)
   #val = conDB.insertPDF(idPDF, nameHTMLGDPR)

   # for file in os.listdir("pdfs/"):
   #    if file == nameHTML.split("/")[1] or file == nameXML.split("/")[1] or file == nameHTMLGDPR.split("/")[1] or file == htmlaScan:
   #          os.remove(file)
   #app.logger.error("do scans " + str(pdf)) 
   
    


# # Instantiation of inherited class
# pdf = PDF()
# pdf.alias_nb_pages()
# pdf.add_page()
# pdf.set_font('Times', '', 12)
# for i in range(1, 41):
#     pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
# pdf.output('report.pdf', 'F')

# pdfObj = pdfGen.PDF(swName, nameCountry)
        # pdfObj.add_page()
        # pdfObj.parseData(content, swPath)
        # pdfObj.output('report.pdf', 'F')