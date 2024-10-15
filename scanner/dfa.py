"""Graph based fsm"""

import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import List, Dict, Tuple, Any


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_accept = False
        self.type = None


class DFA:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.initial_state = None
        self.current_state = None
        self.accept_states = set()
        self.state_map = {}  # Maps trie nodes to DFA states

    def build_trie(self, accepting_tokens, types):
        # accepting tokens and types should zip together
        pass

    def add_state(self, state, is_accept=False):
        self.graph.add_node(state)
        if is_accept:
            self.accept_states.add(state)
        if self.current_state == None:
            self.current_state = state
            self.initial_state = state

    def add_transition(self, from_state, to_state, char):

        for _, _, data in self.graph.out_edges(from_state, data=True):
            if data.get("char") == char:
                raise ValueError(f"Can't add multiple edges for the same char from this node")

        self.graph.add_edge(from_state, to_state, char)

    def set_initial_state(self, state):
        self.current_state = state
        self.initial_state = state

    def process_input(self, input_string):
        # reset dfa
        self.current_state = self.initial_state

        for index, char in enumerate(input_string):
            valid_transition = False

            for _, neighbor, data in self.graph.out_edges(self.current_state, data=True):
                if data.get("char") == char:
                    print(f"Step {index + 1}: On '{char}', transitioning from '{self.current_state}' to '{neighbor}'.")
                    self.current_state = neighbor
                    valid_transition = True
                    break

            if not valid_transition:
                print("No transition found.")

            if self.current_state in self.accept_states:
                print("Input accepted.")
                return True
            else:
                print("Input not accepted.")
                return False


def build_trie(token_sequences: list, types: list) -> TrieNode:
    root = TrieNode()
    for tokens, type_ in zip(token_sequences, types):
        current = root
        for token in tokens:
            if token not in current.children:
                current.children[token] = TrieNode()
            current = current.children[token]
        current.is_accept = True
        current.accept_type = type_
    return root


if __name__ == "__main__":
    type_tokens = [
        "Any",
        "bool",
        "Callable",
        "complex",
        "dict",
        "float",
        "frozenset",
        "int",
        "list",
        "Optional",
        "range",
        "set",
        "str",
        "tuple",
        "Union",
        "NoneType",
    ]
    trie_root = build_trie()
