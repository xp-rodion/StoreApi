FROM python:3.10

ENV PYTHONDONTBYWRITECODE 1
ENV PYTHONUNBUFFED 1

WORKDIR /api

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /api
