# from socket import socket, AF_INET, SOCK_STREAM
# import logging
#
#
# class TestClient:
#     def __init__(self, host, port):
#         self.logger = self._setup_logger()
#         self.host = host
#         self.port = port
#
#     def test_connection(self):
#         data = 'test1'
#         self.socket.send(data.encode())
#         recv_data = self.socket.recv(1024).decode()
#         self.logger.debug(f"Data from server: {str(recv_data)}")
#
#     def send_command(self):
#         data = 'crawl --websites fakt --crawls-amount 1'
#         self.socket.send(data.encode())
#         recv_data = self.socket.recv(1024).decode()
#         self.logger.debug(f"Data from server: {str(recv_data)}")
#
#     def open_conncetion(self):
#         self.socket = self._setup_socket(self.host, self.port)
#
#     def close_connection(self):
#         self.socket.close()
#
#     @staticmethod
#     def _setup_socket(host, port):
#         sock = socket(AF_INET, SOCK_STREAM)
#         sock.connect((host, port))
#         return sock
#
#     @staticmethod
#     def _setup_logger():
#         logger = logging.getLogger('test_client')
#         logger.addHandler(logging.StreamHandler())
#         logger.setLevel(logging.DEBUG)
#         return logger
