"""Graph based fsm"""

import networkx as nx
import matplotlib.pyplot as plt


class DFA:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.initial_state = None
        self.current_state = None
        self.accept_states = set()

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
                if data.get('char') == char:
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
                
