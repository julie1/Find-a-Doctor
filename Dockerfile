FROM python:3.12-slim

WORKDIR /app

RUN pip install pipenv

COPY Find-a-Doctor/data/hip_surgeons.csv Find-a-Doctor/data/hip_surgeons.csv

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --ignore-pipfile --system

COPY Find-a-Doctor .

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 app:app
