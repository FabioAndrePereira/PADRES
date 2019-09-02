from fpdf import FPDF, HTMLMixin
import conDB as conDB

class PDF(FPDF, HTMLMixin):

    def __init__(self, sw, country):
        FPDF.__init__(self, 'P', 'mm', 'A4')
        self.sw = sw
        self.country = country

    def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 20)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'GDPR report for ' + self.sw + ' following the ' + self.country + '\'s specific rules', 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def parseData(self, data, path):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 0, 'Principles', 0, 0, 'L')
        principlesOUT = data["principle"]
        html = ""
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
                    html += """<li>""" + rules[i]["ruleDef"] + """ ---> """ 
                    if rules[i]["ruleCheck"]:
                        html += "In compliance"
                    else:
                        html += "Not in compliance\n"
                        html += "<h6>Suggestions to be in compliance</h6>"
                        html += """
                        <ul>
                            <li>TODO</li>
                        </ul>
                        """
                    html += """</li>"""
                    
                   
            else:
                html +=  "<li>No principles defined</li>" 
            html += "</ul>"
        print(html)
        self.write_html(html)



# <ul>
#                 <li> """ + rules[0]["ruleDef"] + """ </li>
#                 <li> """ + rules[1]["ruleDef"] + """ </li>
#                 <li> """ + rules[2]["ruleDef"] + """ </li>
#             </ul>

