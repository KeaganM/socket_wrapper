import socket

import sys

import errno

from sender import Sender


class Client:
    def __init__(self, HOST='127.0.0.1', PORT=65000):
        self._host = HOST
        self._port = PORT

    def start_client(self, messages):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self._host, self._port))
        client_socket.setblocking(False)

        while True:
            try:
                # msg = input('what is your message?: ')
                # print(msg)
                    while messages:
                        msg = messages.pop()
                        print(msg)
                        client_socket.sendall(msg.get_message())
                # client_socket.sendall(message.send())
            except IOError as e:
                # these are some errors we might see depending on the os if there are no more messages
                # but we are expecting some of these so we want to handle these appropriately
                # really we don't care for these errors so keep this program running
                # if both errors are present then just skip
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('reading error', str(e))
                    sys.exit()
                continue


if __name__ == '__main__':
    m = ['hello from the client', 'hi from the client', 'yo from the client']

    header = {
        'content-type': 'text/json',
        'content-encoding': 'utf-8',
    }

    messages = [Sender(item,**header) for item in m]

    c = Client()
    print('starting the client')
    c.start_client(messages)
    print('hi')
