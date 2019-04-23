import random as rand

def random_bin():
    return rand.randint(0, 100) % 2

def random_float(end):
    return round(rand.uniform(0, end), 4)

def random_porcentual():
    return rand.randint(0, 100) / 100

def random_int(start, end):
    return rand.randint(start, end)