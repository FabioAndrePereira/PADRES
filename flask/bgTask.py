import sqlite3 as sql3
import pdfkit
import buildPDF
import time
from flask import Flask, abort, request
import nmapScan
import zap
import subprocess

#trata de fazer todos os scans assim como construir o pdf
def doAllScans(ipTarget, htmlGDPR, timestamp, idPDF):
    # perform nmap scan
    out = nmapScan.nmapScan(ipTarget)
    nameXML = "pdfs/" + str(idPDF) + ".xml"
    nameHTML = "pdfs/" + str(idPDF) + ".html"
    with open("pdfs/" + str(idPDF) + ".xml", "w") as file:
       file.write(out)

    process = subprocess.call(['xsltproc', nameXML, '-o', nameHTML ])
    # perform zap scan
    htmlaScan =  zap.doScan(ipTarget, idPDF)
    # build final pdf
    nameHTMLGDPR = "pdfs/" + str(idPDF) + "-gdpr.html"
    with open(nameHTMLGDPR, "w") as file:
       file.write(htmlGDPR)

    reportName = 'pdfs/report-' + str(idPDF) + '.pdf'
    pdfkit.from_file([nameHTMLGDPR, nameHTML, "pdfs/" + htmlaScan], reportName)  
    # inserir na db
    #fazer clear na pasta pdfs
    return
