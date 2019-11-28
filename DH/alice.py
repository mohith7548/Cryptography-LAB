#!/usr/bin/python3
import socket
from config import p, g, alice_add, bob_add, choose_private_key, compute_public_key, compute_shared_secret_key


def main():
    print('This is Alice, p = {}; g = {}'.format(p, g))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as alice:
        alice.bind(alice_add)
        alice.listen()

        conn, _ = alice.accept()

        # send Name
        conn.send(b'Hey, Alice here!')
        # receive name
        print(conn.recv(1024).decode())

        # choose private key
        a = choose_private_key()
        print('private key:', a)

        # compute public key
        A = compute_public_key(a)
        print('public key:', A)
        
        # send A
        conn.send(str(A).encode())

        # Receive B
        B = int(conn.recv(1024).decode())
        print('Received from Bob:', B)

        # compute shared secret key
        K = compute_shared_secret_key(a, B)

    print(K)


if __name__ == "__main__":
    main()