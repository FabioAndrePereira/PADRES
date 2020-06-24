import pdfkit
import conDB as conDB
import os
import shutil
from datetime import datetime
from PyPDF2 import PdfFileReader
import cookieS

def buildPDF(data, swName, nameCountry):
    html ="""
        <!DOCTYPE html>
        <html>
            <body>
                <h1>GDPR report for """ + swName + """ following the """ + nameCountry  + """\'s specific rules</h1>     
        """
    principlesOUT = data["principle"]
    allRules = 0
    allNotComplianceRules = 0
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

        html += "<h2><font color=\"black\">" + principleHname + "</h2>"
        
        rules = principlesOUT[pID]["rules"]
        
        #organize rules into comply or not
        inCompliance = []
        not_inCompliance = []
        for i in range(0, len(rules)):
            if rules[i]["ruleCheck"]:
                inCompliance.append(rules[i])
            else:
                not_inCompliance.append(rules[i])
        if pID != 7:
            allRules = allRules +  len(rules)
            allNotComplianceRules = allNotComplianceRules + len(not_inCompliance)
        #display rules
        if (len(rules)) > 0:
            html += "<h3><font color=\"green\"> In compliance with: </h2>"
            html += "<ul>"
            for i in range(0, len(inCompliance)):
                html += """<li><font color=\"black\"> """ + inCompliance[i]["ruleDef"] + "</li>"
            html += "</ul>"    

            html += "<h3><font color=\"red\"> Not in compliance with: </h2>"
            html += "<ul>"
            for i in range(0, len(not_inCompliance)):
                html += """<li><font color=\"black\"> """ + not_inCompliance[i]["ruleDef"] + "</li>"
                idDEF = not_inCompliance[i]["ruleID"]
                con = None
                try: 
                    con = conDB.newCon()
                    if(pID != 7): # exclude rule for country
                        res = conDB.getSuggestion(con, idDEF).fetchall()
                        if len(res) == 0:
                            html += "<h5><font color=\"black\"> No suggestions available </font></h5>"
                        else:
                            html += "<h5><font color=\"black\"> Suggestions to be in compliance </font></h5>"
                            html += "<ul>"
                            for k in res:
                                html += """<li><font color=\"black\"> """ + k[1] + "</li>"
                            html += "</ul>"
                            html += "<br>"
                            html += "<p></p>"

                except Exception as e:
                    raise
                finally:
                    if con is not None:
                        try:
                            con.close()
                            print("con closed {}".format(con))
                        except Exception as e:
                            print("Error closing con {}".format(e))   
            html += "</ul>"       
        else:
            html +=  "No principles defined" 

    html += "<h3>The software " + swName + "does not comply with " + str(allNotComplianceRules) + " rules from a total of " + str(allRules) + "</h3>"

    html += """
            </body>
        </html>
    """    
    
    curr = datetime.now()
    timestamp = curr.strftime("%d/%m/%Y %H:%M:%S")
    timestamp = timestamp.replace("/","-").replace(":", "-")
    
    return html, timestamp
    # with open("file.html", "w") as file:
    #         file.write(html)
    # curr = datetime.now()
    # timestamp = curr.strftime("%d/%m/%Y %H:%M:%S")
    # timestamp = timestamp.replace("/","-").replace(":", "-")
    # pdfname = timestamp + '.pdf'
    # #pdfkit.from_file('file.html', 'out.pdf')
    # ['file1.html', 'file2.html']
    # os.rename('out.pdf', pdfname)
    # # insert db
    # con = None
    # try: 
    #     con = conDB.newCon()
    #     conDB.insertPDF(con, countryID, swID, timestamp, pdfname)
    # except Exception as e:
    #     raise
    # finally:
    #     if con is not None:
    #         try:
    #             con.close()
    #             print("con closed {}".format(con))
    #         except Exception as e:
    #             print("Error closing con {}".format(e))
    # shutil.move(pdfname, 'pdfs/')
    #os.remove("file.html")
