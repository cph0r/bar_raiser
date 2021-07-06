FROM python:3
ENV PYTHONUNBUFFERED=1
# WORKDIR /code
RUN mkdir /app
WORKDIR /app
ADD . /app/

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /app/