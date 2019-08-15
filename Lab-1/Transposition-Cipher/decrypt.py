#!/usr/bin/python3

from math import ceil

KEY = None
MATRIX = []
key_pos_map = {}


def _initialize():
    MATRIX.append(list(KEY))
    for i, c in enumerate(KEY):
        key_pos_map[int(c)] = i


def Decrypt(C, KEY):
    _initialize()
    P = ""
    rows = ceil(len(C) / len(KEY))
    for _ in range(rows):
        MATRIX.append([None] * len(KEY))
    print(MATRIX)
    i = 0
    words = []
    while i < len(C):
        words.append(C[i : i + rows])
        i = i + rows
    print(words)
    for col, word in enumerate(words):
        word = list(word)
        c = key_pos_map[col + 1]
        print(word, c)
        for i in range(rows):
            MATRIX[i + 1][c] = word[i]

    print(MATRIX)

    for i in range(rows):
        P = P + "".join(MATRIX[i + 1])

    return P


def main():
    global KEY
    KEY = "4312567"  # input('Enter Key: ')
    C = "TTNAAPTMTSUOAODWCOIZKNLZPETZ"  # input('Enter Cipher: ')
    P = Decrypt(C, KEY)
    print(P)


if __name__ == "__main__":
    main()
