# business Dockerfile

FROM python:3.6

WORKDIR /yk_business

ADD requirments.txt /requirments.txt
RUN pip install -U -r /requirments.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

