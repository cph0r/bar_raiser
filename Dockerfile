FROM python:3

ENV PYTHONBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
COPY . /app 

RUN adduser -D dockuser
RUN chown dockuser:dockuser -R /app/
USER dockuser
