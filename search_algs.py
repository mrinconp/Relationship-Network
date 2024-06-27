from typing import TypeVar, List, Optional, Callable, Set

T = TypeVar('T')

class Stack():
    def __init__(self) -> None:
        self._container = []

    @property
    def empty(self) -> bool:
        return not self._container
    
    def push(self, item) -> None:
        self._container.append(item)

    def pop(self):
        return self._container.pop()


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[T]:
    frontier: Stack[T] = Stack()
    frontier.push(initial)
    explored: Set[T] = {initial}

    while not frontier.empty:
        current : T = frontier.pop()

        if goal_test(current):
            return current

        for child in successors(current):
            if child in explored:
                continue
            frontier.push(child)
            explored.add(child)
    
    return None