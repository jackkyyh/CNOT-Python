import networkx as nx
import numpy as np



def ROW_OP(A, ctrl, tar):
    A[tar] = (A[tar] + A[ctrl])%2
    return ((ctrl, tar),)


def get_layout_graph(layout_file):
    G = nx.Graph()
    with open('res/layout/'+layout_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            q1, q2 = line.split(' ')
            G.add_edge(int(q1), int(q2))
    return G


def parse_circ_qasm(circ_file):
    with open('res/in/'+circ_file, 'r') as f:
       lines = f.readlines()

    num_qubits = int(lines[0])
    circ = [num_qubits]

    for line in lines[1:]:
        line = line.strip().split(' ')
        if(line[0] == 'CNOT'):
            gate, qu1, qu2 = line
            qu1, qu2 = int(qu1), int(qu2)
            circ.append(('CNOT', qu1, qu2))
        else:
            # continue
            gate, qu = line
            qu = int(qu)
            circ.append((gate, qu))

    return circ


def build_parity_mtx(parsed_circ):
    A = np.identity(parsed_circ[0], dtype=int)

    for gate_line in parsed_circ[1:]:
        if(gate_line[0] == 'CNOT'):
            qu1, qu2 = gate_line[1], gate_line[2]
            A[qu2] = (A[qu1] + A[qu2])%2
        else:
            print('Non-CNOT gate occurred!')
        
    return A

def draw(G):
    nx.draw(G, with_labels=True)



def generate_random_circuit(num_qubit, num_cnot=10):
    with open('res/in/'+'rand.txt', 'w') as f:
        f.write(f'{num_qubit} \n')
        for _ in range(num_cnot):
            q1, q2 = np.random.choice(num_qubit, 2, replace=False)
            f.write(f'CNOT {q1} {q2}\n')