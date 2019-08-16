"""
This program cracks the KEY,
    GIVEN: Algorithm, Cipher, Encrypted
"""


def Encrypt(K, P):
    cipher = []
    for letter in P:
        cipher.append(chr((ord(letter) - 65 + K) % 26 + 65))
    return "".join(cipher)


def Crack(C, P):
    key = -1
    while key <= 25:
        key += 1
        if C == Encrypt(key, P):
            break
    return key


def main():
    cipher = input("Enter Cipher Text: ")
    plain = input("Enter Plain Text: ")
    key = Crack(cipher, plain)
    print("Key =", key)


if __name__ == "__main__":
    main()
