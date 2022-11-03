from collections import defaultdict, deque
from collections.abc import Mapping
from typing import Generic, TypeVar

import pygraphviz as pgv

from ._utils.dot_parsing import *
from ._utils.dot_writing import format_nfa
from ._utils.epsilon import EPSILON
from .dfa import DFA

T = TypeVar("T")
S = TypeVar("S")
Alphabet = frozenset[T]
States = frozenset[S]
Transitions = Mapping[tuple[S, T], States]


class NFA(Generic[T, S]):
    def __init__(
            self,
            *,
            states: States,
            alphabet: Alphabet,
            initial: S,
            transition: Transitions,
            final_states: States,
    ):
        self._closures = {s: self.get_closure(s, transition) for s in states}
        self._hoisted_transition = self.hoist_closures(
            states, transition, self._closures
        )
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.transition = transition
        self.final_states = frozenset(
            s for s in states if len(final_states & self._closures[s]) != 0
        )

    def accepts(self, *seq: T) -> bool:
        current = set(self._closures[self.initial])
        for elt in seq:
            current = set().union(*(
                self._hoisted_transition.get((s, elt), set()) for s in current
            ))
        return len(current & self.final_states) != 0

    def to_dfa(self) -> DFA[T, frozenset[S]]:
        new_transition = {}
        new_states = {self._closures[self.initial]}
        queue = deque(new_states)
        while queue:
            current = queue.pop()
            for elt in self.alphabet:
                s1 = frozenset().union(*(
                    self._hoisted_transition.get((s, elt), set())
                    for s in current
                ))
                if s1 and s1 not in new_states:
                    queue.append(s1)
                if s1:
                    new_transition[(current, elt)] = s1
                    new_states.add(s1)
        new_final = frozenset(s for s in new_states if s & self.final_states)
        return DFA(
            alphabet=self.alphabet,
            states=frozenset(new_states),
            initial=self._closures[self.initial],
            transition=new_transition,
            final_states=new_final,
        )

    @classmethod
    def from_dot(cls, data: str) -> "NFA[str, str]":
        g = pgv.AGraph(string=data)
        return cls(
            alphabet=alphabet_of(g),
            states=states_of(g),
            initial=initial_state_of(g),
            transition=nondeterministic_transitions_of(g),
            final_states=finial_states_of(g),
        )

    def to_dot(self):
        return format_nfa(self)

    @staticmethod
    def hoist_closures(
            states: S, transition: Transitions, closures: Mapping[S: States],
    ) -> Transitions:
        transitions = defaultdict(set)
        for state in states:
            for (s, t), s1 in transition.items():
                if s in closures[state] and t != EPSILON:
                    transitions[(state, t)] |= s1
        return {k: frozenset(v) for k, v in transitions.items()}

    @staticmethod
    def get_closure(state: S, transition: Transitions) -> States:
        closure = {state}
        queue = deque(closure)
        while queue:
            current = queue.pop()
            next_ = transition.get((current, EPSILON), frozenset())
            queue += next_ - closure
            closure |= next_
        return frozenset(closure)
