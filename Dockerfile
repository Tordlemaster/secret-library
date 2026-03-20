FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

RUN pip install --no-cache-dir -r requirements.txt

# update packages
RUN apt-get -qq update
RUN apt-get install --yes apache2 apache2-dev
RUN pip install mod_wsgi

RUN mkdir /code
WORKDIR /code

COPY . /code/

EXPOSE 8000

CMD mod_wsgi-express start-server /secret_library/sl_main/wsgi.py --user www-data --group www-data