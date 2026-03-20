FROM python:3.13-slim


RUN mkdir /code
WORKDIR /code

COPY . /code/

ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

RUN pip install --no-cache-dir -r ./requirements.txt


EXPOSE 8000

WORKDIR /code/secret_library

CMD gunicorn sl_main.wsgi:application --bind 0.0.0.0:8000 --workers 3