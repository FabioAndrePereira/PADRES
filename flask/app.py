import sqlite3 as sql3
from flask import Flask, abort, request
from flask_cors import CORS
import jsonParser as jsonParser
import pdfGenerator as pdfGen
import conDB as conDB
import buildPDF
import zap as zapM
import pdfkit
from rq import Queue
from redis import Redis
from rq.job import Job


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
redis_conn = Redis()
q = Queue(connection=redis_conn)

PATH_DB = 'gdpr.db'

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
    from bgTask import doAllScans
    job = q.enqueue(doAllScans, args=(request,PATH_DB))
    print(job.result)
    print(job.get_id())
    response = app.response_class(
        status=202
    )
    return response

@app.route('/tryREDIS', methods=['GET'])
def tryREDIS():
    from bgTask import doAllScans
    job = q.enqueue(doAllScans)
    print(job.result)
    print(job.get_id())
    response = app.response_class(
        status=202
    )
    return response

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key,connection=redis_conn)
    return str(job.result), 200
    

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



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