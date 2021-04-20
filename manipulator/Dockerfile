FROM python:3.9-alpine

ENV MANIPULATOR_PORT=4001

WORKDIR /app

COPY . /app

CMD /bin/sh -c "python manipulator.py --host $MANIPULATOR_HOST --port $MANIPULATOR_PORT"