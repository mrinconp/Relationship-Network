from network import Network
from person import Person
import networkx as nx
import matplotlib.pyplot as plt
from search_algs import dfs, bfs
from typing import Literal, TypeVar
import time

T = TypeVar('T')

def create_random_network(n: int = 50, t: float=0.5) -> Network:
    #t for thickness must be between 0 and 1 inclusive
    vertex = [Person() for _ in range(n)]
    network = Network([])
    network.add_vertices(vertex)
    network.generate_edges(t)

    return network

def plot_network(network: Network) -> None:

    G = network.network_to_nxgraph()
    pos = nx.spring_layout(G)  # get the position using the spring layout algorithm

    plt.rcParams['figure.figsize'] = [10, 10]
    nx.draw_networkx(G, pos = pos, with_labels=False, 
                    node_size=15, width=0.3, node_color='blue', edge_color='grey')
    plt.axis('off')
    plt.show()

def search_for(network: Network, start: T, key: str, value: str, alg: Literal['dfs', 'bfs'] = dfs):
    """Search for a vertex that satisfies the condition <vertex.key == value> using dfs or bfs"""
    
    def goal_test(current):
        #Define goal_test to pass to search alg
        return getattr(current, str(key)) == str(value)
    
    node = alg(start, goal_test, network.neighbors_for_vertex)[0]

    order = list(network.index_of(vertex) for vertex in alg(start, goal_test, network.neighbors_for_vertex)[1]) #make order based on nodes index
    return (node, order)

def visualize_search(order, G, pos):
    plt.figure()

    node_color = ['b' for _ in range(len(G.nodes))]
    for i, node in enumerate(order, start=0):
        plt.clf()

        ind = list(G.nodes).index(node)
        node_color[ind] = 'r'

        nx.draw(G, pos, with_labels = False, node_color = node_color, node_size = 15, width=0.3, edge_color = 'gray')
        plt.draw()
        plt.pause(0.5)
    plt.show()
    time.sleep(0.5)

def run(graph_type: Literal['network', 'tree'] = 'network', plot = True, animate = False):
    if graph_type == 'network':

        network = create_random_network()
        satisfied = search_for(network, network._vertices[5], "city", "Bogota", dfs)[0] #node that meets criteria

        order1 = search_for(network, network._vertices[5], "city", "Bogota", dfs)[1] #LIFO
        order2 = search_for(network, network._vertices[5], "city", "Bogota", bfs)[1] #FIFO

        if satisfied:
            print("Found one person that meets criteria:")
            satisfied.show_attributes()
        else:
            print("There isn't any related person that meets the criteria")
            
        G = network.network_to_nxgraph()
        pos = nx.spring_layout(G) 

        if plot:
            plot_network(network)

    elif graph_type == 'tree':
        G = nx.random_tree(20)
        pos = nx.spring_layout(G) 
        order1 = dfs(1,None, successors= G.neighbors)[1]
        order2 = bfs(1,None, successors= G.neighbors)[1]

    if animate:
        visualize_search(order1, G, pos)
        print(f"Algoritmo DFS. Número de iteraciones: {len(order1)}")
        visualize_search(order2, G, pos)
        print(f"Algoritmo BFS. Número de iteraciones: {len(order2)}")


run(graph_type='network', plot=True, animate=True)