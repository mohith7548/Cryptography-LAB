#!/usr/bin/python3
from math import ceil

KEY = None
MATRIX = []
key_pos_map = {}


def _initialize():
    global KEY, key_pos_map
    KEY = "4312567"  # input('Enter Key: ')
    for i, c in enumerate(KEY):
        key_pos_map[int(c)] = i

    MATRIX.append(list(KEY))


def Encypt(P, KEY):
    n = len(KEY)
    m = len(P)
    print(m, n, 7 - m % n)
    P = P + (7 - m % n) * "Z"
    print(P)
    i = 0
    while i <= m:
        MATRIX.append(list(P[i : i + n]))
        i = i + n
    print(MATRIX)
    C = ""
    for i in range(n):
        col = [MATRIX[x + 1][key_pos_map[i + 1]] for x in range(ceil(m / n))]
        print(col)
        C = C + "".join(col)
    return C


def main():
    _initialize()
    print(KEY, MATRIX)
    P = "ATTACKPOSTPONEDUNTILTWOAM"  # input("Enter a Plain Text: ")
    C = Encypt(P, KEY)
    print(C)


if __name__ == "__main__":
    main()
