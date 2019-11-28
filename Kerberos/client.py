#!/usr/bin/python3
import socket
from utils.config import *


def main():
    print('This is Client')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(AS_ADD)
        
        # send request for a server

        # recv T



if __name__ == "__main__":
    main()