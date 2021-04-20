import argparse
import logging
import socketserver


logging.basicConfig(encoding='utf-8', format='%(levelname)s:\t%(message)s', level=logging.INFO)


class ManipulatorHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).decode('utf-8')
        logging.info(data)


def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse()

    with socketserver.TCPServer((args.host, args.port), ManipulatorHandler) as server:
        server.serve_forever()
