import networkx as nx
import numpy as np

def get_steiner_tree(G, terminals):
    st = nx.algorithms.approximation.steinertree.steiner_tree(G, terminals)
    steiner = G.subgraph(st.nodes)
    return steiner


def trim_by_layer(tree, root):
    layers = []
    cur = None
    for parent, children in nx.bfs_successors(tree, root):
        for child in children:
            if(cur is None or parent in cur[:,1]):
                layers.append(cur)
                cur = np.zeros([0, 2], dtype=int)
            cur = np.append(cur, ((parent, child),), axis=0)
            # print(cur.shape)
    layers.append(cur)
    layers.pop(0)
    return layers

def seperate_dfs(Tc, node, visited, terminals, Tg):
    T_list = []
    
    create_tree = Tc is None
    if(create_tree):
        Tc = nx.Graph()
        Tc.add_node(node)

    neighbors = list(Tg.neighbors(node))
    # if(parent is not None):
    #     neighbors.remove(parent)
    # print(f'In {node}, neighbors: {neighbors}')

    for n in neighbors:
        if(n in visited):
            continue
        # Tc.add_node(n)
        Tc.add_edge(node, n)
        if(len(list(Tg.neighbors(n))) > 1):
            if(n in terminals):
                T_list += seperate_dfs(None, n, visited + [node], terminals, Tg)
            else:
                T_list += seperate_dfs(Tc, n, visited + [node], terminals, Tg)
    if(create_tree):
        T_list.append((Tc, node))
    return T_list

def get_leaves(G, root):
    pass