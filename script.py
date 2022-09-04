import sys
from algorithms import *
from utils import *
from graph import *


sys.setrecursionlimit(100)

G = get_layout_graph('6.txt')

# generate_random_circuit(6, 20)
in_circ = parse_circ_qasm('rand.txt')
A_init = build_parity_mtx(in_circ)
print(A_init)

A = A_init.copy()
Y1 = fix_upper(A, G.copy())

A = A.transpose()
print(A)
Y2 = fix_lower(A, G.copy())
Y = Y2 + Y1
# print(A)