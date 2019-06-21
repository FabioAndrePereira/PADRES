import sqlite3 as sql3

PATH_DB = 'gdpr.db'

class dbConnection:
    dbCon = None

    def newConnection(self):
        try:
            dbCon = sql3.connect(PATH_DB)
        except sql3.Error as e:
            print("Error ---> {}".format(e))
            raise

    def getRulesbySWiD(self):
        cursor = self.dbCon.cursor()
        cursor.e

