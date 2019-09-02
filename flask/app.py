import sqlite3 as sql3
from flask import Flask, abort, request
from flask_cors import CORS
import jsonParser as jsonParser
import pdfGenerator as pdfGen
import conDB as conDB
import buildPDF

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
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
        print(e)
        abort(500, {'message': e})
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
                app.logger.info("dbcon closed {}".format(dbCon))
            except Exception as e:
                app.logger.error("Error closing con {}".format(e))
    try:
        html = buildPDF.buildPDF(content, swName, nameCountry)        
        # pdfObj = pdfGen.PDF(swName, nameCountry)
        # pdfObj.add_page()
        # pdfObj.parseData(content, swPath)
        # pdfObj.output('report.pdf', 'F')
    except Exception as e:
        print(e)
        abort(500, {'message': e})

    response = app.response_class(
        status=201
    )
    return response


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

