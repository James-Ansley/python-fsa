from collections import defaultdict, deque
from collections.abc import Mapping
from typing import Generic, TypeVar

import pygraphviz as pgv
import sentinel

from dfa import DFA
from utils.dot_parsing import *

T = TypeVar("T")
S = TypeVar("S")


class NFA(Generic[T, S]):
    epsilon = sentinel.create("epsilon")

    def __init__(
            self,
            *,
            states: frozenset[S],
            alphabet: frozenset[T],
            initial: S,
            transition: Mapping[tuple[S, T], frozenset[S]],
            final_states: frozenset[S],
    ):
        closures = {
            s: self.get_closure(s, transition, self.epsilon)for s in states
        }
        final = {s for s in states if len(final_states & closures[s]) != 0}

        self.alphabet = alphabet
        self.states = states
        self.initial = closures[initial]
        self.transition = self.hoist_transitions(
            states, transition, self.epsilon, closures
        )
        self.final_states = frozenset(final)

    def accepts(self, *seq: T) -> bool:
        current = set(self.initial)
        for elt in seq:
            current = set().union(
                *(self.transition.get((s, elt), set()) for s in current)
            )
        return len(current & self.final_states) != 0

    def to_dfa(self) -> DFA:
        new_transition = {}
        new_states = {self.initial}
        queue = deque((self.initial,))
        while queue:
            current = queue.pop()
            for elt in self.alphabet:
                s1 = (self.transition.get((s, elt), set()) for s in current)
                s1 = frozenset().union(*s1)
                if s1 and s1 not in new_states:
                    queue.append(s1)
                if s1:
                    new_transition[(current, elt)] = s1
                    new_states.add(s1)
        new_final = frozenset(s for s in new_states if s & self.final_states)
        return DFA(
            alphabet=self.alphabet,
            states=frozenset(new_states),
            initial=self.initial,
            transition=new_transition,
            final_states=new_final,
        )

    @classmethod
    def from_dot(cls, data: str):
        g = pgv.AGraph(string=data)
        return cls(
            alphabet=alphabet_of(g),
            states=states_of(g),
            initial=initial_state_of(g),
            transition=nondeterministic_transitions_of(g),
            final_states=finial_states_of(g),
        )

    @staticmethod
    def hoist_transitions(
            states: S,
            transition: Mapping[tuple[S, T], frozenset[S]],
            epsilon: object | T,
            closures: Mapping[S: frozenset[S]]
    ) -> Mapping[tuple[S, T], frozenset[S]]:
        transitions = defaultdict(set)
        for state in states:
            for (s, t), s1 in transition.items():
                if s in closures[state] and t != epsilon:
                    transitions[(state, t)] |= s1
        return {k: frozenset(v) for k, v in transitions.items()}

    @staticmethod
    def get_closure(
            state: S,
            transition: Mapping[tuple[S, T], frozenset[S]],
            epsilon: object | T,
    ) -> frozenset[S]:
        closure = {state}
        queue = deque(closure)
        while queue:
            current = queue.pop()
            next_ = transition.get((current, epsilon), frozenset())
            queue += next_ - closure
            closure |= next_
        return frozenset(closure)
