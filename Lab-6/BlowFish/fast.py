import sys
import base64
from Crypto.Cipher import Blowfish
from struct import pack


class BlowfishCipher(object):
    def __init__(self, key):
        self.bs = Blowfish.block_size
        self.cipher = Blowfish.new(key, Blowfish.MODE_ECB)

    def encrypt(self, plaintext):
        # padding = self._pad(plaintext)
        encrypted = self.cipher.encrypt(plaintext)
        encoded = base64.b64encode(encrypted)
        return str(encoded, 'utf-8')

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        return str(decrypted, 'utf-8')

    def _pad(self, s):
        # return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        plen = self.bs - len(s) % self.bs
        padding = [plen] * plen
        padding = pack('b'*plen, *padding)
        return padding

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


if __name__ == '__main__':
    # key = '`?.F(fHbN6XK|j!t'
    key = input('Enter Key: ')
    cipher = BlowfishCipher(key)

    # plaintext = '542#1504891440039'
    plaintext = input('Enter Plaintext: ')
    encrypted = cipher.encrypt(plaintext)
    print('Encrypted: %s' % encrypted)
    # ciphertext = '5bgJqIqFuT8ACuvT1dz2Bj5kx9ZAIkODHWRzuLlfYV0='
    # assert encrypted == ciphertext

    decrypted = cipher.decrypt(encrypted)
    print('Decrypted: %s' % decrypted)
    # assert decrypted == plaintext