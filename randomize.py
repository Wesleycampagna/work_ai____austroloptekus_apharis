import random as rand

# ------------------------------------------------------------------------------------------
#    Alunos:    William Felipe Tsubota      - 2017.1904.056-7
#               Wesley Souza Campagna       - 2014.1907.010-0
#               Alberto Benites             - 2016.1906.026-4
#               Gabriel Chiba Miyahira      - 2017.1904.005-2
# ------------------------------------------------------------------------------------------

def random_bin():
    return rand.randint(0, 100) % 2

def random_float(end):
    return round(rand.uniform(0, end), 4)

def random_porcentual():
    return rand.randint(0, 100) / 100

def random_int(start, end):
    return rand.randint(start, end)