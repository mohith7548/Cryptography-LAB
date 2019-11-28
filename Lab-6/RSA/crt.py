#!/usr/bin/python3

def extended_euclidean(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_euclidean(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = extended_euclidean(a, m)
    return x % m


def crt(m, x):

    while True:


        temp1 = modinv(m[1], m[0]) * x[0] * m[1] + \
                modinv(m[0], m[1]) * x[1] * m[0]

        # temp2 contains the value of the modulus
        # in the new equation, which will be the
        # product of the modulii of the two
        # equations that we are combining
        temp2 = m[0] * m[1]

        # we then remove the first two elements
        # from the list of remainders, and replace
        # it with the remainder value, which will
        # be temp1 % temp2
        x.remove(x[0])
        x.remove(x[0])
        x = [temp1 % temp2] + x

        # we then remove the first two values from
        # the list of modulii as we no longer require
        # them and simply replace them with the new
        # modulii that we calculated
        m.remove(m[0])
        m.remove(m[0])
        m = [temp2] + m

        # once the list has only one element left,
        # we can break as it will only contain
        # the value of our final remainder
        if len(x) == 1:
            break

    # returns the remainder of the final equation
    return x[0]


# driver segment
# m = [3,5]
# x = [2,3]
m = [1927, 187, 667]
x = [292, 146, 663]
print(crt(m, x))