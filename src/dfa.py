from collections.abc import Mapping
from typing import Generic, TypeVar

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
