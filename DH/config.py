#!/usr/bin/python3

'''
All coniguration detatils are present here

Alice acts as server & 
Bob acts as client

'''

p = 23
g = 5

alice_add = ('localhost', 4444)
bob_add = ('localhost', 5555)

private_key_range = 20


def choose_private_key():
    import random
    return random.randint(1, private_key_range)


def compute_public_key(x):
    return (g**x) % p


def compute_shared_secret_key(x, Y):
    '''
    x:= a and Y:= B (or) 
    x:= b and Y:= A
    '''
    return (Y**x) % p