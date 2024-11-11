FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install --upgrade pip

# packages required for setting up WSGI
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libc-dev python3-dev default-libmysqlclient-dev libpcre3 libpcre3-dev build-essential pkg-config
RUN pip install mysqlclient
RUN pip install uwsgi -I --no-cache-dir
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# copy project
COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:5002"]


