#!/usr/bin/python3
from sys import exit
from AffineCipher import Encrypt, Decrypt

msg = """
Choose an Option:
    0. exit
    1. Encrypt
    2. Decrypt
>> """


def main():
    key = input("Enter the key (a, b): ").split(",")
    key = [int(x) for x in key]
    print(key)
    while True:
        option = int(input(msg))
        if option == 0:
            exit(0)
        elif option == 1:
            P = input("Enter PlainText: ").upper()
            C = Encrypt(key, P)
            print("CipherText =", C)
        elif option == 2:
            C = input("Enter CipherText: ").upper()
            P = Decrypt(key, C)
            print("PlainText =", P)
        else:
            print("Choose correct option!")


if __name__ == "__main__":
    main()
