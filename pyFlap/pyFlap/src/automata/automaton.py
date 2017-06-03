import collections
import pickle

from automata.node import Node
from automata.transition import Transition, LAMBDA


class Automaton:
    def __init__(self):
        self.nodes = []
        self.transitionNames = []

    def is_nfa(self):
        nondeterministic_states = self._get_nondeterministic_states()
        return len(nondeterministic_states) > 0

    def add_node(self):
        node = Node(len(self.nodes))
        node.x = 100
        node.y = 100
        self.nodes.append(node)
        return node

    def set_node_state(self, index, new_state):
        self.nodes[int(index)].state = new_state

    def _get_nondeterministic_states(self):
        list = []
        for node in self.nodes:
            if node.transitions:
                for i, transition in enumerate(node.transitions):
                    if self._is_lambda_transition(transition):
                        if list.count(node) == 0:
                            list.append(node)
                    else:
                        for transition2 in node.transitions[i + 1:]:
                            if self._are_nondeterministic(transition, transition2):
                                if list.count(node) == 0:
                                    list.append(node)
        return list

    def _is_lambda_transition(self, transition: Transition):
        return transition.name == LAMBDA

    def _are_nondeterministic(self, transition_one: Transition, transition_second: Transition):
        if transition_one.name == transition_second.name:
            return True
        if transition_one.name.startswith(transition_second.name):
            return True
        if transition_second.name.startswith(transition_one.name):
            return True

    def save(self, url):
        with open(url, 'wb') as output:
            pickle.dump(self.nodes, output, pickle.HIGHEST_PROTOCOL)

    def load(self, url):
        self.nodes = pickle.load(open(url, "rb"))
