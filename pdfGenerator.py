from fpdf import FPDF

class PDF(FPDF):

    def __init__(self, sw, country):
        FPDF.__init__(self, 'P', 'mm', 'A4')
        self.sw = sw
        self.country = country

    def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
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
        self.multi_cell(0, 5, data)

