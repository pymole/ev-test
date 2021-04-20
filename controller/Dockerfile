FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

# copy project
COPY . /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libpq g++

RUN pip install -r requirements.txt