FROM python:3.9

RUN mkdir /app
WORKDIR /app
COPY fsk.txt /app/fsk.txt
RUN pip3 install -r /app/fsk.txt
COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]