import pdfkit
import conDB as conDB
import pdfkit
import os

def buildPDF(data, swName, nameCountry):
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
        try: 
            con = conDB.newCon()
            res = conDB.getPrincipleHname(con, principleHid)
            for i in res:
                principleHname = i[1]
        except Exception as e:
            raise
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
    pdfkit.from_file('file.html', 'out.pdf')
    os.remove("file.html")