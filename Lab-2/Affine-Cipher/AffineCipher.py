"""
Implementation of Affine Cipher
"""

# Extended Euclidean Algorithm for finding modular inverse
# eg: modinv(7, 26) = 15
def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    # gcd, x, y = egcd(a, m)
    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def Encrypt(K, P):
    """Encrypts PlainText with given Key and return the Cipher
    """
    P = [ord(x) - 65 for x in list(P)]
    C = [(K[0] * x + K[1]) % 26 for x in P]
    C = [chr(x + 65) for x in C]
    C = "".join(C)
    return C


def Decrypt(K, C):
    """Decrypts Cipher to Plaintext with given Key
    """
    C = [ord(x) - 65 for x in list(C)]
    P = [((x - K[1]) * modinv(K[0], 26)) % 26 for x in C]
    P = [chr(x + 65) for x in P]
    P = "".join(P)
    return P
