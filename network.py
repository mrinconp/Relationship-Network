from edge import Edge
from person import Person
from itertools import combinations
from typing import TypeVar, Generic, List, Optional

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
        for vertix in vertices:
            self._vertices.append(vertix)
            self._edges.append([])

    def index_of(self, vertix: V) -> int:
        return self._vertices.index(vertix)

    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())

    def generate_edges(self, thickness:float) -> None:
        comb = list(combinations(self._vertices,2))
        for element in comb:
            u, v = [self.index_of(element[i]) for i in [0,1]]
            edge = Edge(u,v)
            self.add_edge(edge)

vertix = [Person() for _ in range(2)]
network = Network([])
network.add_vertices(vertix)
network.generate_edges(1)
for person in network._vertices:
    print(person.show_atributes())
