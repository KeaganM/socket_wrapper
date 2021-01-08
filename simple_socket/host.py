import socket
import json
import select

from typing import Callable, Union

import time


class Receiver:
    _header_length = None
    _header = None

    def __init__(self, proto_header_len: int = 10):
        self._proto_header_length = proto_header_len
        self.buffer = ''

    def process(self, data) -> Union[None, str]:

        self.buffer += data.decode('utf-8')

        try:
            if not self._header_length and len(self.buffer) >= self._proto_header_length:
                self._process_decorator(self._process_proto_header, self._proto_header_length)

            if not self._header and len(self.buffer) >= self._header_length:
                self._process_decorator(self._process_header, self._header_length)

            if len(self.buffer) >= int(self._header['content-length']):
                msg = json.loads(self.buffer)
                self._clean()
                return msg
        except TypeError:
            pass
        return None

    def _process_decorator(self, process_f: Callable, start_index: int) -> None:
        process_f()
        self._truncate_buffer(start_index)

    def _process_proto_header(self) -> None:
        self._header_length = int(self.buffer[:self._proto_header_length].strip())

    def _process_header(self) -> None:
        self._header = json.loads(self.buffer[:self._header_length])

    def _truncate_buffer(self, start_index: int) -> None:
        self.buffer = self.buffer[start_index:]

    def _clean(self) -> None:
        self.buffer = ''
        self._header_length = None
        self._header = None

    def __repr__(self):
        return f'{self.__dict__}'


class Server:
    _socket_list = []
    _clients = dict()

    def __init__(self, HOST: str = '127.0.0.1', PORT: int = 65000):
        self._host = HOST
        self._port = PORT

    def start_server(self):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self._host, self._port))
        server_socket.listen()

        self._socket_list.append(server_socket)

        while True:
            read_sockets, _, exception_sockets = select.select(self._socket_list, [], self._socket_list)

            for notified_socket in read_sockets:
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    print(f'connected to client from {client_address[0]}:{client_address[1]}')

                    data = client_socket.recv(1024)
                    r = Receiver()
                    res = r.process(data)

                    while not res:
                        data = client_socket.recv(1024)
                        res = r.process(data)
                    print(res)


if __name__ == '__main__':
    s = Server()
    s.start_server()
