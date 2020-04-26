import sqlite3 as sql3

PATH_DB = 'gdpr.db'

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

    

def newCon():
    return sql3.connect(PATH_DB)

def getPrinciplesHeaders(dbCon):
    cursor = dbCon.cursor()
    queryPh = 'SELECT * FROM principleHeader ORDER BY id'
    data = cursor.execute(queryPh)
    
    return data

def getPrinciples(dbCon, phID):
    cursor = dbCon.cursor()
    queryPrinciples = 'SELECT principle.id, principle.definition FROM principle ' \
                          'WHERE principle.principleHeaderID = ?;'
    data = cursor.execute(queryPrinciples, phID)

    return data

def getPrincipleHname(dbCon, phID):
    cursor = dbCon.cursor()
    queryPrinciples = 'SELECT * FROM principleHeader ' \
                            'WHERE principleHeader.id = ?;'
    data = cursor.execute(queryPrinciples, phID)

    return data

def createPDFentry(dbCon, countryID, swID, timestamp, status=0):
    # with open(timestamp + ".html", "w") as file:
    #     file.write(pdfs)

    # blobPDF = convertToBinaryData(timestamp + ".html")
    queryInsert = 'INSERT INTO genPDFs(countryID, softID, timestamp, status) VALUES(?, ?, ?, ?)'
    cur = dbCon.cursor()
    ret = cur.execute(queryInsert, (countryID, swID, timestamp, status))
    dbCon.commit()
    return ret.lastrowid

def insertJobID(dbCon, jobID, pdfID):
    # with open(timestamp + ".html", "w") as file:
    #     file.write(pdfs)

    # blobPDF = convertToBinaryData(timestamp + ".html")
    queryInsert = 'UPDATE genPDFs SET job_id = ? WHERE id = ?'
    cur = dbCon.cursor()
    cur.execute(queryInsert, (jobID, pdfID))
    dbCon.commit()
    
def getPDFs(dbCon):
    cur = dbCon.cursor()
    pdfsQuery = 'SELECT * from genPDFs ' \
                'join country c on genPDFs.countryID = c.id ' \
                'join software s on genPDFs.softID = s.id;'
    data = cur.execute(pdfsQuery)

    return data

def insertPDF(idPDF, pdfName): # faz update na tabela pdf depois de acabar o job
    conDB = None
    pdfBLOB = convertToBinaryData(pdfName)
    try:
        dbCon = sql3.connect(PATH_DB)
        queryInsert = 'UPDATE genPDFs SET pdfs = ? and status = 1 WHERE id = ?'
        cur = dbCon.cursor()
        cur.execute(queryInsert, (pdfBLOB, idPDF))
    except Exception as e:
        pass
    finally:
        if dbCon is not None:
            try:
                dbCon.close()
            except Exception as e:
                print("Error closing con {}".format(e))
    
    
