FROM node:14.5.0

# add `/app/node_modules/.bin` to $PATH
#ENV PATH /app/gdprinterface/node_modules/:$PATH
WORKDIR /app/gdprinterface

COPY package.json /app/gdprinterface/package.json
RUN npm install
RUN npm install -g @angular/cli@8 --unsafe

COPY . /app/gdprinterface


CMD ng serve --host 0.0.0.0
