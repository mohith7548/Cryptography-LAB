#!/usr/bin/python3
from aes import AESCipher

# Note AES key must be 16/24/32 bytes coressponding to AES-128/192/256
class Message():
    def __init__(self, msg):
        self.msg = msg

    def encrypt(self, key):
        cipher = AESCipher(key)
        self.msg = cipher.encrypt(self.msg)

    def decrypt(self, key):
        cipher = AESCipher(key)
        self.msg = cipher.decrypt(self.msg)

    def __str__(self):
        return self.msg


if __name__ == "__main__":
    msg = Message('Hii')
    msg.encrypt('1234567890qwerty')
    print(msg)
    msg.decrypt('1234567890qwerty')
    print(msg)