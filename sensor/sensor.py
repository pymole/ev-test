import argparse
import json
import logging
import socket
import time
import urllib.request
import urllib.error
import random
import datetime
from json import JSONEncoder


logging.basicConfig(encoding='utf-8', format='%(levelname)s:\t%(message)s', level=logging.INFO)


def generate_message():
    datetime_payload = datetime.datetime.now()

    simulate_delay = random.randint(1, 100) < 10
    if simulate_delay:
        datetime_payload -= datetime.timedelta(seconds=random.randint(10, 60))

    payload = random.randint(0, 100)

    return {
        'datetime': datetime_payload,
        'payload': payload,
    }


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def send_message(message: dict, url: str):
    encoded_message = json.dumps(message, cls=DateTimeEncoder).encode('utf-8')
    headers = {
        'Content-Length': len(encoded_message),
        'Content-Type': 'application/json; charset=utf-8',
    }

    request = urllib.request.Request(
        url,
        encoded_message,
        headers,
        method='POST',
    )

    try:
        response = urllib.request.urlopen(request)
    except (urllib.error.URLError, socket.error) as e:
        logging.info(e)


def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('--url', type=str)
    parser.add_argument('--timeout', type=float, default=0.003)

    return parser.parse_args()


def main():
    args = parse()

    while True:
        message = generate_message()
        send_message(message, args.url)
        time.sleep(args.timeout)


if __name__ == '__main__':
    main()
