FROM python:3.13-slim


RUN mkdir /code
WORKDIR /code

COPY . /code/

ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

RUN pip install --no-cache-dir -r ./requirements.txt

RUN mkdir /code/secret_library/sl_media
RUN mkdir /code/secret_library/sl_media/save_files
RUN mkdir /code/secret_library/sl_media/media
RUN mkdir /code/secret_library/sl_media/media/gamedata
RUN mkdir /code/secret_library/db

#RUN chown -R 568:568 /code/secret_library/sl_media
#RUN chown -R 568:568 /code/secret_library/db

#USER 568:568

WORKDIR /code/secret_library

EXPOSE 8000

CMD python3 manage.py migrate && python3 manage.py loaddata sl_main/fixtures/users.json && gunicorn sl_main.wsgi:application --bind 0.0.0.0:8000 --workers 3
#gunicorn sl_main.wsgi:application --bind 0.0.0.0:8000 --workers 3
#python3 manage.py runserver 0.0.0.0:8000