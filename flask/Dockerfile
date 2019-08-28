FROM python:3-onbuild

COPY . /app

#WORKDIR /app/flaskGDPR

RUN pip install -r requirements.txt

#ENTRYPOINT ["python"]

CMD ["python", "app.py"]