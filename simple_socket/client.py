import socket
import select
from dataclasses import dataclass
from typing import Any, Union, ByteString
import json


class Message:
    def __init__(self, content: str, proto_header_len: int = 10, **headers):
        self.content = {'data': content}

        self.headers = headers
        self.headers.update({'content-length': len(json.dumps(self.content))})

        self._proto_header_len = proto_header_len

    def send(self):
        # if type == 'header':
        header = self._prep_to_send(self.headers)
        message = self._prep_to_send(self.content)
        return f'{len(header):<{self._proto_header_len}}{header}{message}'.encode('utf-8')
        # else:
        #     return self._prep_to_send(self.content).encode('utf-8')

    def _prep_to_send(self, header_or_content: dict):
        message = {key: value for key, value in header_or_content.items()}
        return json.dumps(message)

    def __repr__(self):
        return f'{self.__dict__}'


class Client:
    def __init__(self, HOST='127.0.0.1', PORT=65000):
        self._host = HOST
        self._port = PORT

    def start_client(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self._host, self._port))
        client_socket.setblocking(False)

        # header
        client_socket.send(message.send())
        # # message
        # client_socket.send(message.send('message'))


if __name__ == '__main__':
    m = 'hello from the client'

    header = {
        'content-type': 'text/json',
        'content-encoding': 'utf-8',
    }

    message = Message(m, **header)
    # r = message.send('header')
    # print(r)

    c = Client()
    print('starting the client')
    c.start_client(message)
