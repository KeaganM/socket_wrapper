import socket
import select

class Client:
    def __init__(self,HOST='127.0.0.1',PORT=65000):
        self._host = HOST
        self._port = PORT

    def start_client(self):
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((self._host,self._port))
        client_socket.setblocking(False)

        client_socket.send(b'hello from the client')


if __name__ == '__main__':
    c = Client()
    pass
