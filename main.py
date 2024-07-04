from network import Network
from person import Person
import networkx as nx
import matplotlib.pyplot as plt
from search_algs import dfs
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

    G, pos = network.network_to_nxgraph()

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

    order = (network.index_of(vertex) for vertex in alg(start, goal_test, network.neighbors_for_vertex)[1]) #make order based on nodes index
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

def run(plot = True, animate = False):
    network = create_random_network()
    satisfied, order = search_for(network, network._vertices[5], "city", "Bogota")
    if satisfied:
        print("Found one person that meets criteria:")
        satisfied.show_attributes()
    else:
        print("There isn't any related person that meets the criteria")
        
    G, pos = network.network_to_nxgraph()

    if plot:
        plot_network(network)
    if animate:
        visualize_search(order, G, pos)


run(plot=True, animate=True)