# Dockerfile

FROM python:3.6

WORKDIR /scrapy_book

ADD requirements.txt /requirements.txt
RUN pip install -U -r /requirements.txt


