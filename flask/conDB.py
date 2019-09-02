import sqlite3 as sql3

PATH_DB = 'gdpr.db'

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