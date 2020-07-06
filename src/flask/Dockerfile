FROM ubuntu:18.04
COPY . /app
#RUN apt-get update && apt-get install -y xvfb  && apt-get install -y wkhtmltopdf
#RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz


# # install google chrome
RUN apt-get update
RUN apt-get install -y wget \  
    gnupg2
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y \ 
    google-chrome-stable \
    xsltproc \
    nmap \
    xvfb \
    python3-pip \
    curl \
    unzip


ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# install chromedriver
WORKDIR /app
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#RUN cp chromedriver -d /usr/local/bin/


 

RUN tar -xJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wk* /usr/local/bin/

RUN pip3 install -r requirements.txt



#CMD ["python", "app.py" ]