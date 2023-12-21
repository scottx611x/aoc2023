from dataclasses import dataclass
from typing import List, Set

import networkx as nx
import time

start = time.time()

G = nx.DiGraph()


with open("input.txt") as f:
    for idx, line in enumerate(f.readlines()):
        line = line.strip("\n")

        if not line:
            continue

        if idx == 0:
            lefty_righty = line
            continue

        _id, left_right = line.replace(" ", "").split("=")
        left, right = left_right.replace("(", "").replace(")", "").replace(" ", "").split(",")

        G.add_node(_id)
        G.add_edge(_id, left)
        G.add_edge(_id, right)


class WastelandTraverser:
    def __init__(self, graph: nx.DiGraph, start_node: str = "AAA", traversal_sequence: str = lefty_righty, end_node: str = "ZZZ"):
        self.graph = graph
        self.traversal_sequence = traversal_sequence

        self.start_node = start_node
        self.end_node = end_node

        self.camel_steps_taken = 0
        self.sequence_index = 0

    def _get_next_move(self) -> int:
        self.camel_steps_taken += 1

        # Account for continuously wrapping around the LR inputs
        next_move = 0 if self.traversal_sequence[self.sequence_index % len(self.traversal_sequence)] == "L" else 1
        self.sequence_index = (self.sequence_index + 1) % len(self.traversal_sequence)

        return next_move

    def ride_camel(self) -> int:
        node = self.start_node

        while node != self.end_node:

            neighbors = list(self.graph.neighbors(node))

            # Account for duplicate "neighbors" like: "CDD = (QVN, QVN)"
            if len(neighbors) < 2:
                neighbors *= 2

            node = neighbors[self._get_next_move()]

        return self.camel_steps_taken


camel_steps_taken = WastelandTraverser(G).ride_camel()

print(camel_steps_taken)
print('It took', time.time() - start, 'seconds.')