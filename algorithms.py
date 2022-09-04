import networkx as nx
import numpy as np
from graph import get_steiner_tree, seperate_dfs, trim_by_layer
from utils import ROW_OP, draw




def fix_diag(A, idx, G):
    print('fix diag', idx)
    v = np.where(A[idx:, idx] == 1)[0] + idx
    terminals = np.append(v, idx)
    steiner = get_steiner_tree(G, terminals)
    for b_it in nx.bfs_successors(steiner, idx):
        for neib in b_it[1]:
            if(neib in v) :
                return ROW_OP(A, neib, idx)


def fix_upper(A, G):
    Y = []
    for idx in range(len(A)):
        if(A[idx, idx] == 0):
            Y += fix_diag(A, idx, G)

        terminals = np.where(A[idx:, idx] == 1)[0] + idx
        # print(terminals)
        if(len(terminals) > 1):
            
            print(A)
            steiner = get_steiner_tree(G, terminals)
            # if(idx == 2):
            #     draw(steiner)
            # print('edges', steiner.edges)
            # print('nodes', G.nodes)
            T_list = seperate_dfs(None, idx, [], terminals, steiner)
            for T, root in T_list:
                print('T:', T.edges)
                Yc = ROW_OP_V(A, T, root)
                Y += Yc
                print(Yc)
        
        G.remove_node(idx)
    
        print(f'finished upper {idx}')
        print(A)
        # print()

                        
    return list(reversed(Y))

def fix_lower(A, G):
    Y = []
    for idx in range(len(A)):
        print(f'idx {idx}')
        terminals = np.where(A[idx:, idx] == 1)[0] + idx
        if(len(terminals) <= 1):
            G.remove_node(idx)
            continue
        
        steiner = get_steiner_tree(G, terminals)
        T_list = seperate_dfs(None, idx, [], terminals, steiner)
        for T, root in T_list:
            Yc = ROW_OP_M(A, T, root)
            Y += Yc
            print(Yc)
            
        B = {}
        for T, root in reversed(T_list):
            non_leaves = nx.dfs_successors(T, root).keys()
            # print(non_leaves)
            for n in T.nodes():
                if(n not in non_leaves):
                    B[n] = root
                    # print(f'leave {n}, root {root}')
                    croot = root
                    while(n < croot):
                        steiner = get_steiner_tree(G, [croot, n])
                        Yc =  ROW_OP_M(A, steiner, croot)
                        Y += Yc
                        print('correction', Yc)
                        # print('correction:', Yc, 'steiner', [croot, n])
                        croot = B[n] = B[croot]
    
        # print(f'finished lower {idx}')
        # print(A)
        # print()

        G.remove_node(idx)
    Y = [(tar, ctrl) for (ctrl, tar) in Y]
    return Y


def ROW_OP_V(A, T, root):
    Y = []
    layers = trim_by_layer(T, root)
    for layer in layers:
        for edge in layer:
            Y += ROW_OP(A, edge[0], edge[1])
    for layer in reversed(layers[:-1]):
        for edge in layer:
            Y += ROW_OP(A, edge[0], edge[1])
    return Y

def ROW_OP_M(A, T, root):
    Y = []
    layers = trim_by_layer(T, root)
    
    for layer in reversed(layers[1:]):
        for edge in layer:
            Y += ROW_OP(A, edge[0], edge[1])
    for layer in layers:
        for edge in layer:
            Y += ROW_OP(A, edge[0], edge[1])
    for layer in reversed(layers[:-1]):
        for edge in layer:
            Y += ROW_OP(A, edge[0], edge[1])
    for layer in layers[1:-1]:
        for edge in layer:
            Y += ROW_OP(A, edge[0], edge[1])

    return Y