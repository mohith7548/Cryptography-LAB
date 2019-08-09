#!/usr/bin/python3

KEY = ""
MATRIX = [[None for _ in range(5)] for _ in range(5)]

cols = [[None for _ in range(5)] for _ in range(5)]


def initialize():
    # alphabet set
    alphabet_set = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]

    # contruct MATRIX
    k, c = 0, 0
    for i in range(5):
        for j in range(5):
            if k < len(KEY):
                MATRIX[i][j] = KEY[k]
                alphabet_set.remove(KEY[k])
                k += 1
            else:
                if alphabet_set[c] == "I":
                    MATRIX[i][j] = "I"
                    alphabet_set.remove("J")
                else:
                    MATRIX[i][j] = alphabet_set[c]
                c += 1
            cols[j][i] = MATRIX[i][j]

    for i in range(5):
        for j in range(5):
            if MATRIX[i][j] == "I":
                print("I/J", end="\t")
            else:
                print(MATRIX[i][j], end="\t")
        print()
    print()


def get_pos(l):
    if l == "J":
        return get_pos("I")
    for i in range(5):
        for j in range(5):
            if MATRIX[i][j] == l:
                return i, j
    return -1, -1


def is_same_col(x, y):
    for i in range(len(cols)):
        if x in cols[i] and y in cols[i]:
            return True, i, (cols[i].index(x), cols[i].index(y))
    return False, -1, (-1, -1)


def is_same_row(x, y):
    for i in range(5):
        if x in MATRIX[i] and y in MATRIX[i]:
            return True, i, (MATRIX[i].index(x), MATRIX[i].index(y))
    return False, -1, (-1, -1)


def validate_constraints(text):
    text = list(text)
    # 1. Repeating letters get 'X' inserted in the Middle
    to_be_inserted_at = []
    for i in range(len(text) - 1):
        if text[i] == text[i + 1]:
            to_be_inserted_at.append(i + 1)

    for pos in to_be_inserted_at:
        text.insert(pos, "X")

    # 2. If length of text is odd => append 'X'
    if len(text) % 2 != 0:
        text.append("X")

    return "".join(text)


def Encrypt(plain_text):
    print(plain_text)
    text = validate_constraints(plain_text)
    print(text)
    cipher = []
    i = 0
    while i < len(text):
        print(text[i], text[i + 1])
        row_res = is_same_row(text[i], text[i + 1])
        col_res = is_same_col(text[i], text[i + 1])
        # print(row_res, col_res)
        if row_res[0]:
            row = row_res[1]
            col = row_res[2]
            print("same row", row, col)
            cipher.append(MATRIX[row][(col[0] + 1) % 5])
            cipher.append(MATRIX[row][(col[1] + 1) % 5])
            # print(cipher)

        elif col_res[0]:
            col = col_res[1]
            row = col_res[2]
            print("same col", row, col)
            cipher.append(MATRIX[(row[0] + 1) % 5][col])
            cipher.append(MATRIX[(row[1] + 1) % 5][col])
            # print(cipher)

        else:
            print("else")
            x = get_pos(text[i])
            y = get_pos(text[i + 1])
            print(x, y)
            if x == y:
                tmp = MATRIX[(x[0] + 1) % 5][(x[1] + 1) % 5]
                print(tmp)
                cipher.append(tmp)
                cipher.append(tmp)
            else:
                cipher.append(MATRIX[x[0]][y[1]])
                cipher.append(MATRIX[y[0]][x[1]])
            # print(cipher)

        i += 2
    return "".join(cipher)


def main():
    global KEY
    print("Playfair Cipher Encryption Alg\n")

    KEY = input("Enter the Key: ").upper()
    print()

    initialize()

    plain_text = input("Enter a string: ").upper()
    print()

    cipher = Encrypt(plain_text)
    print(cipher)


if __name__ == "__main__":
    main()
