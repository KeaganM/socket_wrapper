import socket
import sys
import errno

from sender import Sender

class MessageContainer:
    def __init__(self):
        self.messages = ['intial message']

    def pop(self):
        return self.messages.pop()

    def push(self,item):
        self.messages.append(item)

    def __repr__(self):
        return f'messages: {self.messages}'

class Client:
    def __init__(self, HOST='127.0.0.1', PORT=65000):
        self._host = HOST
        self._port = PORT

    def start_client(self, message_object:MessageContainer,header:dict):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self._host, self._port))
        client_socket.setblocking(False)

        while True:
            try:
                # msg = input('what is your message?: ')
                # print(msg)
                    while message_object.messages:
                        msg = Sender(message_object.pop(),**header).get_message()
                        client_socket.sendall(msg)
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

    import threading
    import time

    def inputter(message_container: MessageContainer):
        while True:
            user_input = input('what to put into the container?: ')
            message_container.push(user_input)
            if 'quit' in user_input:
                return None


    m = MessageContainer()
    print('starting client')
    c = Client()

    header = {
        'content-type': 'text/json',
        'content-encoding': 'utf-8',
    }
    # c.start_client(m,header)
    t1 = threading.Thread(target=inputter,args=[m])
    t2 = threading.Thread(target=c.start_client,args=[m,header])

    t1.start()
    t2.start()

    # def test2(message_container:MessageContainer):
    #     while True:
    #         time.sleep(1)
    #         print(message_container)
    #         if 'quit' in message_container.messages:
    #             return None
    #
    #
    # t1 = threading.Thread(target=test1,args=[m])
    # t2 = threading.Thread(target=test2,args=[m])
    #
    # t1.start()
    # t2.start()





    # # m = ['hello from the client', 'hi from the client', 'yo from the client']
    #
    # # messages = [Sender(item,**header) for item in m]
    #
    # def create_message(message,message_object:list):
    #
    #     message_object.append(message)
    #     return message_object
    #
    # header = {
    #     'content-type': 'text/json',
    #     'content-encoding': 'utf-8',
    # }
    #
    #
    # c = Client()
    # print('starting the client')
    #
    # t1 = threading.Thread(target=c.start_client,args=[MESSAGES,header])
    #
    # # c.start_client(MESSAGES,header)
    #
