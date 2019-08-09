#!/usr/bin/python3


def disp(K):
    for i in range(0, 25):
        print(chr(i + 65), end=" ")

    print()
    for i in range(0, 25):
        print(chr((i + K) % 26 + 65), end=" ")

    print()


def Encypt(K, P):
    cipher = []
    for letter in P:
        cipher.append(chr((ord(letter) - 65 + K) % 26 + 65))
    return "".join(cipher)


def main():
    print("Ceaser Cipher Encryption Alg")
    key = int(input("Enter Key: "))
    disp(key)
    plain_text = input("Enter Plain Text: ").upper()
    cipher_text = Encypt(key, plain_text)
    print(cipher_text)


if __name__ == "__main__":
    main()
