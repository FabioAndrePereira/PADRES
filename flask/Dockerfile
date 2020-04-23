FROM python:3-onbuild
COPY . /app

RUN pip3 install -r requirements.txt
#RUN apt-get update && apt-get install -y xvfb  && apt-get install -y wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wk* /usr/local/bin/
#sudo apt-get install libxml2-dev



#ENTRYPOINT ["python"]

#WORKDIR /app/flaskGDPR

CMD ["python", "app.py" ]