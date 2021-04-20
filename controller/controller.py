import os
from itertools import islice
import asyncio
import datetime
import socket
import json
from json import JSONEncoder

from aioredis.pubsub import Receiver

import models
from database import context_session
import settings
import cache


last_command_datetime_key = 'last-command-datetime'


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class Controller:
    def __init__(self):
        self.receiver = Receiver()
        self.marks = []

        self.last_average_payload = 0

    async def reader(self):
        await cache.connection.subscribe(self.receiver.channel('marks'))

        async for channel, message in self.receiver.iter():
            mark = json.loads(message)
            self.marks.append(mark)

    async def control(self):
        status_data = self.get_status()
        if status_data is None:
            return

        status, average_payload, aggregated_marks_number = status_data
        status_datetime = datetime.datetime.now()

        try:
            self.send(status, status_datetime)
        except socket.error:
            return

        await self.update(status, average_payload, status_datetime, aggregated_marks_number)

    def get_status(self):

        if not self.marks:
            return None

        aggregated_marks_number = len(self.marks)

        average_payload = sum(
            mark['payload']
            for mark in islice(self.marks, aggregated_marks_number)
        )/aggregated_marks_number

        status = 'down' if average_payload < self.last_average_payload else 'up'

        return status, average_payload, aggregated_marks_number

    async def update(self, status: str, average_payload: float,
                     status_datetime: datetime.datetime,
                     aggregated_marks_number: int):

        self.last_average_payload = average_payload
        self.marks = self.marks[aggregated_marks_number:]

        with context_session() as db:
            command = models.Command(status=status, datetime=status_datetime)
            db.add(command)
            db.commit()

        await cache.connection.set(last_command_datetime_key, status_datetime.isoformat())

    def send(self, status: str, datetime: datetime.datetime):
        payload = {
            'datetime': datetime,
            'status': status,
        }
        encoded_payload = json.dumps(payload, cls=DateTimeEncoder).encode('utf-8')

        conn = socket.create_connection(
            (settings.global_settings.manipulator_host, settings.global_settings.manipulator_port)
        )
        conn.sendall(encoded_payload)
        conn.close()


def get_controller():
    return Controller()


async def periodic(coro, interval):
    while True:
        await coro()
        await asyncio.sleep(interval)


async def run():
    await cache.init_cache()

    controller = get_controller()
    asyncio.ensure_future(controller.reader())
    asyncio.ensure_future(periodic(controller.control, 5))


if __name__ == '__main__':
    asyncio.ensure_future(run())

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
