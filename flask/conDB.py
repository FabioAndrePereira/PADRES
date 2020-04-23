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

def insertPDF(dbCon, countryID, swID, timestamp, pdfs):
    blobPDF = convertToBinaryData(pdfs)
    queryInsert = 'INSERT INTO genPDFs(countryID, softID, timestamp, pdfs) VALUES(?, ? ,?, ?)'
    cur = dbCon.cursor()
    cur.execute(queryInsert, (countryID, swID, timestamp, blobPDF))
    dbCon.commit()
    
def getPDFs(dbCon):
   #pdfsPATH = "pdfs/"
    cur = dbCon.cursor()
    pdfsQuery = 'SELECT * from genPDFs ' \
                'join country c on genPDFs.countryID = c.id ' \
                'join software s on genPDFs.softID = s.id;'
    data = cur.execute(pdfsQuery)

    return data