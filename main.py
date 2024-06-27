from network import Network
from person import Person
import networkx as nx
import matplotlib.pyplot as plt
from search_algs import dfs
from typing import Literal, TypeVar

T = TypeVar('T')

def create_random_network(n: int = 50, t: float=0.5) -> Network:
    #t for thickness must be between 0 and 1 inclusive
    vertex = [Person() for _ in range(n)]
    network = Network([])
    network.add_vertices(vertex)
    network.generate_edges(t)

    return network

def plot_network(network: Network) -> None:
    G = nx.Graph()

    for edge in network._edges:
        for i in range(len(edge)):
            if edge:
                u = edge[i].u
                v = edge[i].v
                G.add_edge(u,v)

    pos = nx.spring_layout(G) # get the position using the spring layout algorithm

    plt.rcParams['figure.figsize'] = [10, 10]
    nx.draw_networkx(G, pos = pos, with_labels=False, 
                    node_size=15, width=0.3, node_color='blue', edge_color='grey')
    plt.axis
    plt.show()

def search_for(network: Network, start: T, key: str, value: str, alg: Literal['dfs', 'bfs'] = dfs):
    """Search for a vertex that satisfies the condition <vertex.key == value> using dfs or bfs"""
    
    def goal_test(current):
        #Define goal_test to pass to search alg
        return getattr(current, str(key)) == str(value)
    
    return alg(start, goal_test, network.neighbors_for_vertex)

def run():
    network = create_random_network()
    plot_network(network)
    satisfied = search_for(network, network._vertices[5], "city", "Bogota")

    if satisfied:
        print("Found one person that meets criteria:")
        satisfied.show_attributes()
    else:
        print("There isn't any related person that meets the criteria")

run()

