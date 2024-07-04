from edge import Edge
from itertools import combinations
from typing import TypeVar, Generic, List
import math 
import random
import networkx as nx

V = TypeVar('V')
E = TypeVar('E')

class Network(Generic[V]):

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)
    
    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))

    def __init__(self, vertices: List[V]):
        vertices = list(set(vertices)) #Remove duplicated objects
        self._vertices: List[V] = vertices
        self._edges: List[List[V]] = [ [] for _ in self._vertices]

    def add_vertices(self, vertices: List[V]) -> int:
        for vertex in vertices:
            self._vertices.append(vertex)
            self._edges.append([])

    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)
    
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())

    def generate_edges(self, thickness:float) -> None:
        """Generate edges between vertices based on thickness parameter: 
        thickness = 0 -> 0 edges
        thickness = 1 -> all 2-length combinations between vertices"""

        n = self.vertex_count
        spanning_tree_edges = n - 1
        complete_graph_edges = math.comb(n, 2)

        num_edges = int(spanning_tree_edges + thickness * (complete_graph_edges - spanning_tree_edges))

        #Generate spanning tree to avoid disconnected graphs
        remaining_vertices= set(self._vertices)
        current_vertex = remaining_vertices.pop()
        tree_edges = []

        while remaining_vertices:
            next_vertex = remaining_vertices.pop()
            tree_edges.append((current_vertex, next_vertex))
            current_vertex = next_vertex

        for u, v in tree_edges:
            u = self.index_of(u)
            v = self.index_of(v)
            edge = Edge(u,v)
            self.add_edge(edge)

        #Add 2-lenght combinations between all vertices and shuffle to pick randomly
        remaining_edges = list(combinations(self._vertices, 2))
        random.shuffle(remaining_edges)

        #Remove tree edges from combinations to avoid repetition
        for u,v in remaining_edges: 
            if (u, v) in tree_edges or (v,u) in tree_edges:
                remaining_edges.remove((u,v))

        #Add remaining number of edges
        additional_edges = num_edges - len(tree_edges)
        for u,v in remaining_edges[:additional_edges]:
            u = self.index_of(u)
            v = self.index_of(v)
            edge = Edge(u,v)
            self.add_edge(edge)

    def neighbors_for_index(self, index:int) -> List[V]:
        return list(map(self.vertex_at, [edge.v for edge in self._edges[index]]))
    
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))
    
    def network_to_nxgraph(self):
        """Turn network into Nx graph to plot and visualize"""
        G = nx.Graph()
        for edge in self._edges:
            for i in range(len(edge)):
                if edge:
                    u = edge[i].u
                    v = edge[i].v
                    G.add_edge(u,v)

        pos = nx.spring_layout(G)  # get the position using the spring layout algorithm

        return G, pos

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc