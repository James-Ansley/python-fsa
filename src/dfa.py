from collections.abc import Mapping
from typing import Generic, TypeVar

import pygraphviz as pgv

from utils.dot_parsing import *

T = TypeVar("T")
S = TypeVar("S")


class DFA(Generic[T, S]):
    def __init__(
            self,
            *,
            alphabet: frozenset[T],
            states: frozenset[S],
            initial: S,
            transition: Mapping[tuple[S, T], S],
            final_states: frozenset[S],
    ):
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.transition = transition
        self.final_states = final_states

    def accepts(self, *seq: T) -> bool:
        current = self.initial
        for elt in seq:
            current = self.transition.get((current, elt), None)
        return current in self.final_states

    @classmethod
    def from_dot(cls, data: str):
        g = pgv.AGraph(string=data)
        return cls(
            alphabet=alphabet_of(g),
            states=states_of(g),
            initial=initial_state_of(g),
            transition=deterministic_transitions_of(g),
            final_states=finial_states_of(g),
        )
