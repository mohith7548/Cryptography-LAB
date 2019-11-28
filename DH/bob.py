#!/usr/bin/python3
import socket
from config import p, g, alice_add, bob_add, choose_private_key, compute_public_key, compute_shared_secret_key


def main():
    print('This is Bob, p = {}; g = {}'.format(p, g))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bob:
        bob.connect(alice_add)        

        # revc name
        print(bob.recv(1024).decode())
        # send Name
        bob.send(b'Hey, Bob here!')

        # choose private key
        b = choose_private_key()
        print('private key:', b)

        # compute public key
        B = compute_public_key(b)
        print('public key:', B)
        
        # send A
        bob.send(str(B).encode())

        # Receive B
        A = int(bob.recv(1024).decode())
        print('Received from Alice:', A)

        # compute shared secret key
        K = compute_shared_secret_key(b, A)

    print(K)


if __name__ == "__main__":
    main()