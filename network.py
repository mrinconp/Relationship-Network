from edge import Edge
from person import Person
from itertools import combinations
from typing import TypeVar, Generic, List, Optional
import math 
import random

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
        thickness = 1 -> full 2-length combinations between vertices"""

        n = int(thickness * math.comb(self.vertex_count, 2))
        comb = list(combinations(self._vertices, 2))
        random.shuffle(comb)

        for element in comb[:n]: #Take the first n elements of the list
            u, v = [self.index_of(element[i]) for i in [0,1]]
            edge = Edge(u,v)
            self.add_edge(edge)

    def neighbors_for_index(self, index:int) -> List[V]:
        return list(map(self.vertex_at, [edge.v for edge in self._edges[index]]))
    
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc

vertex = ["Bogota","Medellin","Bucaramanga","Cali"]
network = Network([])
network.add_vertices(vertex)
network.generate_edges(0.5)

print(network)
