import pdfkit
from pdfrw import PdfReader
from pdfrw import PdfWriter
import json
#from PyPDF2 import PdfFileReader, PdfFileWriter

name = "pdfs/outx"+"1"+".pdf"
#pdfkit.from_file(['pdfs/try.html'],name )
x = PdfReader('pdfs/out.pdf')

#print(type(x))
#PdfWriter("out1.pdf", trailer=val).write()
