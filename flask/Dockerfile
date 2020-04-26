FROM python:3-onbuild



#RUN apt-get update && apt-get install -y xvfb  && apt-get install -y wkhtmltopdf
#RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar -xJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wk* /usr/local/bin/
RUN apt-get update
RUN apt-get install xsltproc 
RUN apt-get install -y nmap 
RUN pip3 install -r requirements.txt

COPY . /app
#CMD ["python", "app.py" ]