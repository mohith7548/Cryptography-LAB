#!/usr/bin/python3
import socket, threading
from utils.config import *
from utils.kerberos_db import *


class ServerThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        print(self.client)
        self.client.send(b'Hii man!')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as auth_sock:
        auth_sock.bind(AS_ADD)
        auth_sock.listen(MAX_CONNECTIONS)

        while True:
            print('Authentication server Listening...')
            client, addr = auth_sock.accept()
            print('{} connected!'.format(addr))
            ServerThread(client).start()



if __name__ == "__main__":
    main()