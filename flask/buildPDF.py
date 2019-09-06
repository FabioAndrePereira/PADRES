import pdfkit
import conDB as conDB
import os
import shutil
from datetime import datetime
from PyPDF2 import PdfFileReader

def buildPDF(data, swName, nameCountry, countryID, swID):
    html ="""
        <!DOCTYPE html>
        <html>
            <body>
                <h1>GDPR report for """ + swName + """ following the """ + nameCountry  + """\'s specific rules</h1>     
        """
    principlesOUT = data["principle"]
    for pID in range(0, 8): # 8 = numero de principios definidos
        principleHid = principlesOUT[pID]["pID"]
        principleHname = ''
        con = None
        try: 
            con = conDB.newCon()
            res = conDB.getPrincipleHname(con, principleHid)
            for i in res:
                principleHname = i[1]
        except Exception as e:
            raise
        finally:
            if con is not None:
                try:
                    con.close()
                    print("con closed {}".format(con))
                except Exception as e:
                    print("Error closing con {}".format(e))

        html += "<h2>" + principleHname + "</h2>"
        
        rules = principlesOUT[pID]["rules"]
        html += "<ul>"
        if (len(rules)) > 0:
            for i in range(0, len(rules)):
                if rules[i]["ruleCheck"]:
                    html += """<li><font color=\"green\" """ + rules[i]["ruleDef"] + """ --->  In compliance""" 
                else:
                    html += """<li><font color=\"red\" """ + rules[i]["ruleDef"] + """ --->  Not in compliance"""
                    html += "<h6><font color=\"black\"> Suggestions to be in compliance </font></h6>"
                    html += """
                    <ul>
                        <li><font color=\"black\">TODO</font></li>
                    </ul>
                    """
                html += """</font></li>"""
                
                
        else:
            html +=  "<li>No principles defined</li>" 
        html += "</ul>"

    html += """
            </body>
        </html>
    """    
    with open("file.html", "w") as file:
            file.write(html)
    curr = datetime.now()
    timestamp = curr.strftime("%d/%m/%Y %H:%M:%S")
    timestamp = timestamp.replace("/","-").replace(":", "-")
    pdfname = timestamp + '.pdf'
    pdfkit.from_file('file.html', 'out.pdf')
    os.rename('out.pdf', pdfname)
    # insert db
    con = None
    try: 
        con = conDB.newCon()
        conDB.insertPDF(con, countryID, swID, timestamp, os.getcwd() + '/pdfs')
    except Exception as e:
        raise
    finally:
        if con is not None:
            try:
                con.close()
                print("con closed {}".format(con))
            except Exception as e:
                print("Error closing con {}".format(e))
    shutil.move(pdfname, 'pdfs/')
    os.remove("file.html")
