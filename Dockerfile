# Dockerfile


FROM python:3.6

#WORKDIR /scrapy_book

ADD requirements.txt /requirements.txt
ADD  iqiwx  /scrapy_book
ADD  run_spider.py  /scrapy_book
ADD  scrapy.cfg    /scrapy_book
ADD  web_book /web_book
ADD  web_html/dist /static

RUN pip install -U -r /requirements.txt

RUN apt-get update
RUN apt-get install vim -y

RUN apt-get install nginx -y

ADD nginx/default /etc/nginx/sites-enabled/

RUN service nginx restart

