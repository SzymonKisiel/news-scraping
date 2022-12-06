from socket import socket, AF_INET, SOCK_STREAM
import logging

from console_app.program_parser import get_parser
from console_app.program import program


class ScrapingServer:
    def __init__(self, host, port):
        self.logger = self._setup_logger()
        self.socket = self._setup_socket(host, port)

    def run(self):
        self.logger.info("Server is running")

        while True:
            connection, address = self.socket.accept()
            self.logger.debug(f"New connection: {address}")

            while True:
                # max data size: 1024 bytes
                data = connection.recv(1024).decode()
                if not data:
                    break
                self.logger.debug(f"Data from client: {str(data)}")

                # TODO Parse data to command
                parser = get_parser()
                args = {}
                args = parser.parse_args(['crawl', '--websites', 'fakt', '--crawls-amount', '1'])
                # args = parser.parse_args('crawl --websites fakt --crawls-amount 1'.split())
                program(args)

                # TODO Respond to client

                data = 'response'
                connection.send(data.encode())  # send data to the client

    @staticmethod
    def _setup_socket(host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(2)
        return sock

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger('test_server')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger
