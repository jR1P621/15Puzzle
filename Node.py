# KivaGale Hall & Jon Rippe
# Created for CSCE A405 - Artificial Intelligence Fall 2021
# Node Class - node for use in a linked data structure

from typing import List


class Node:
    def __init__(self, state, parent, action, cost: int, depth: int) -> None:
        self.state = state
        self.parent: Node = parent
        self.action = action
        self.cost = cost
        self.depth = depth
        self.children: List[Node] = []

    def __gt__(self, o: object) -> bool:
        if not isinstance(o, Node):
            return False
        return self.cost > o.cost

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Node):
            return False
        return self.cost == o.cost
