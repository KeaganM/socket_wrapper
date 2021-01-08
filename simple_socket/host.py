import socket
import select

from reciever import Receiver


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
            try:
                read_sockets, _, exception_sockets = select.select(self._socket_list, [], self._socket_list)
                r = Receiver()

                for notified_socket in read_sockets:
                    if notified_socket == server_socket:
                        client_socket, client_address = server_socket.accept()

                        self._socket_list.append(client_socket)
                        print(f'connected to client from {client_address[0]}:{client_address[1]}')
                    else:
                        data = notified_socket.recv(1024)
                        res = r.process(data)
                        while not res:
                            data = notified_socket.recv(1024)
                            res = r.process(data)
                        print(res)

            except ConnectionResetError as e:
                print(e)
                continue


if __name__ == '__main__':

    s = Server()
    print('starting the server')
    s.start_server()
