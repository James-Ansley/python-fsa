from collections.abc import Mapping
from typing import Generic, TypeVar

import pygraphviz as pgv

from ._utils.dot_parsing import *
from ._utils.dot_writing import format_dfa

T = TypeVar("T")
S = TypeVar("S")
Alphabet = frozenset[T]
States = frozenset[S]
Transitions = Mapping[tuple[S, T], S]


class DFA(Generic[T, S]):
    def __init__(
            self,
            *,
            alphabet: Alphabet,
            states: States,
            initial: S,
            transition: Transitions,
            final_states: States,
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
    def from_dot(cls, data: str) -> "DFA[str, str]":
        g = pgv.AGraph(string=data)
        return cls(
            alphabet=alphabet_of(g),
            states=states_of(g),
            initial=initial_state_of(g),
            transition=deterministic_transitions_of(g),
            final_states=finial_states_of(g),
        )

    def to_dot(self):
        return format_dfa(self)

    def squash(self):
        return DFA(
            alphabet=self.alphabet,
            states=frozenset(join(s) for s in self.states),
            initial=join(self.initial),
            final_states=frozenset(join(s) for s in self.final_states),
            transition={
                (join(s), t): join(s1) for (s, t), s1 in self.transition.items()
            },
        )


def join(elts):
    return "".join(str(s) for s in sorted(elts))
