FROM python:3.9-alpine

ENV TIMEOUT=0.003

WORKDIR /app

COPY . /app

CMD ["/bin/sh", "-c", "python sensor.py --url $CONTROLLER_URL --timeout $TIMEOUT"]