#!/usr/bin/python3
from AffineCipher import Encrypt, modinv
from math import floor


def Crack(P, C):
    P = [ord(x) - 65 for x in list(P)]
    C = [ord(x) - 65 for x in list(C)]
    print(P, C)
    a = (C[0] - C[1]) / (P[0] - P[1])
    b = (P[0] * C[1] - C[0] * P[1]) / (P[0] - P[1])
    key = [a, b]
    key = (int(a), int(b))
    key = [(x + 26) % 26 for x in key]
    return key


def main():
    print("Known Cipher Text Attack in AffineCipher")
    P = input("Enter PlainText: ").upper()
    C = input("Enter CipherText: ").upper()
    key = Crack(P, C)
    print(key)


if __name__ == "__main__":
    main()
