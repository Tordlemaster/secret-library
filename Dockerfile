FROM python:3.13-slim

RUN mkdir /app && mkdir /app/secret-library
WORKDIR /app/secret-library

COPY secret_library/ /app/secret-library

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN ls

RUN pip install --no-cache-dir -r ./requirements.txt

RUN mkdir /app/secret-library/sl_media
RUN mkdir /app/secret-library/sl_media/save_files
RUN mkdir /app/secret-library/sl_media/media
RUN mkdir /app/secret-library/sl_media/media/gamedata
RUN mkdir /app/secret-library/db

WORKDIR /app/secret-library

EXPOSE 8000

CMD python3 manage.py migrate && python3 manage.py loaddata sl_main/fixtures/users.json && gunicorn sl_main.wsgi:application --bind 0.0.0.0:8000 --workers 3