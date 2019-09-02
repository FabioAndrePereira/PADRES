FROM node:11.15.0

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/gdprinterface/node_modules/.bin:$PATH

#COPY package.json /app/gdprinterface/package.json
#RUN npm install
RUN npm install -g @angular/cli@7.3.8

COPY . /app/gdprinterface

WORKDIR /app/gdprinterface

CMD ng serve --host 0.0.0.0
