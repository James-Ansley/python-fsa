"""
A nondeterministic finite state machine and its corresponding transducer
"""

from collections import defaultdict, deque
from collections.abc import Hashable, Iterable, Mapping
from pprint import pformat
from textwrap import indent
from typing import Final, Generic, Self, TypeVar

__all__ = ["NFA", "NFATransducer"]

from .dfa import DFA

T = TypeVar("T", bound=Hashable)
S = TypeVar("S", bound=Hashable)
V = TypeVar("V", bound=Hashable)
Alphabet = frozenset[T]
States = frozenset[S]
Transitions = Mapping[tuple[S, T], frozenset[S]]


class NFA(Generic[T, S]):
    """
    A nondeterministic finite state machine.

    Allows for transitions to be a partial function – in the case a
    transition is not defined, the state becomes the empty set.

    NFAs are immutable and can only accept or reject whole sequences of tokens.
    However, a mutable NFATransducer can be constructed with the
    :meth:`transducer` method which can accept one token at a time.
    """

    EPSILON: Final[str] = "\u03B5"

    def __init__(
          self,
          *,
          states: Iterable[S],
          alphabet: Iterable[T],
          initial: S,
          transitions: Mapping[tuple[S, T], Iterable[S]],
          final: Iterable[S],
          epsilon: object = EPSILON,
    ):
        self.states: Final[States] = frozenset(states)
        self.alphabet: Final[Alphabet] = frozenset(alphabet)
        self.initial: Final[S] = initial
        self.final: Final[States] = frozenset(final)
        self.epsilon: Final[object] = epsilon
        self.transitions: Final[Transitions] = {
            (s, t): frozenset(s1) for (s, t), s1 in transitions.items()
        }

        closures = \
            {s: _closure_of(s, self.transitions, epsilon) for s in self.states}
        self._flat_final = frozenset().union(*(closures[s] for s in self.final))
        self._flat_transitions = _flatten(
            self.initial,
            self.states,
            self.transitions,
            closures,
            self.epsilon,
        )
        self._flat_initial = closures[self.initial]

    def accepts(self, input: Iterable[T]) -> bool:
        """
        Returns True if the given input is accepted by this NFA and
        False otherwise
        """
        current = self._flat_initial
        transitions = self._flat_transitions
        for e in input:
            current = \
                set().union(*(transitions.get((s, e), set()) for s in current))
        return len(current & self._flat_final) != 0

    def to_dfa(self) -> DFA[T, frozenset[S]]:
        """Transforms this NFA into a DFA"""
        new_transition = {}
        new_states = {self._flat_initial}
        queue = deque(new_states)
        while queue:
            current = queue.pop()
            for elt in self.alphabet:
                s1 = frozenset().union(*(
                    self._flat_transitions.get((s, elt), set())
                    for s in current
                ))
                if s1 and s1 not in new_states:
                    queue.append(s1)
                if s1:
                    new_transition[(current, elt)] = s1
                    new_states.add(s1)
        new_final = frozenset(
            s for s in new_states if s & self._flat_final
        )
        return DFA(
            alphabet=self.alphabet,
            states=frozenset(new_states),
            initial=self._flat_initial,
            transitions=new_transition,
            final=new_final,
        )

    def without_epsilon(self) -> "NFA[T, S]":
        """
        Returns a new NFA with epsilon transitions removed.
        Any unreachable states as a result of this are also removed.
        """
        return NFA(
            alphabet=self.alphabet,
            states={s for (s, _) in self._flat_transitions},
            initial=self.initial,
            transitions=self._flat_transitions,
            final=self.final,
        )

    def transducer(
          self, output: Mapping[S, V] = None) -> "NFATransducer[T, S, V]":
        """
        Returns a transducer with the given output mapping. By default,
        this maps states to a boolean indicating whether the closure of that
        state contains an accepting/final state.
        """
        if output is None:
            output = {s: s in self._flat_final for s in self.states}
        return NFATransducer(
            self._flat_initial,
            self._flat_transitions,
            self._flat_final,
            output,
        )

    def __str__(self):
        return "\n".join((
            "NFA(",
            indent(f"alphabet={pformat(self.alphabet)},", " " * 4),
            indent(f"states={pformat(self.states)},", " " * 4),
            indent(f"initial={pformat(self.initial)},", " " * 4),
            indent(f"transitions={pformat(self.transitions)},", " " * 4),
            indent(f"final={pformat(self.final)},", " " * 4),
            ")",
        ))


class NFATransducer(Generic[T, S, V]):
    """
    A mutable Moore machine that accepts inputs one at a time. The output of
    each "state" is the set of the mapping S -> V for all states, S, in the
    current state set.

    Allows for the NFA transitions to be a partial function – in the case a
    transition is not defined, the state and output become the empty set.
    """

    def __init__(
          self,
          initial: Iterable[S],
          transitions: Transitions,
          final: States,
          output: Mapping[S, V]
    ):
        self._current = frozenset(initial)
        self._transitions = transitions
        self._final = final
        self._output = output

    @property
    def current(self) -> frozenset[S]:
        """The current state set of the transducer"""
        return self._current

    @property
    def output(self) -> frozenset[V]:
        """The current output set of the transducer"""
        return frozenset(self._output[s] for s in self._current)

    @property
    def is_accepting(self) -> bool:
        """Returns True if the transducer is in an accepting state"""
        return len(self._current & self._final) != 0

    def push(self, input: T) -> frozenset[V]:
        """Transitions the transducer and returns the new output set"""
        self._current = frozenset().union(
            *(self._transitions.get((s, input), set()) for s in self._current)
        )
        return self.output


def _closure_of(state: S, transitions: Transitions, epsilon: object) -> States:
    closure = {state}
    queue = deque(closure)
    while queue:
        current = queue.pop()
        next_ = transitions.get((current, epsilon), frozenset())
        queue += next_ - closure
        closure |= next_
    return frozenset(closure)


def _flatten(
      initial: S,
      states: States,
      transitions: Transitions,
      closures: Mapping[S: States],
      epsilon: object,
) -> Transitions:
    result = defaultdict(set)
    for state in states:
        for (s, t), s1 in transitions.items():
            if s in closures[state] and t != epsilon:
                result[(state, t)] |= s1
    return _cull(
        initial,
        {(s, t): frozenset(s1) for (s, t), s1 in result.items()}
    )


def _cull(initial: S, transitions: Transitions) -> Transitions:
    reachable = {initial}
    queue = deque(reachable)
    while queue:
        current = queue.pop()
        next_reachable = set().union(*(
            s1 for (s, _), s1 in transitions.items() if s == current
        ))
        queue.extend(next_reachable - reachable)
        reachable |= next_reachable
    return {(s, t): s1 for (s, t), s1 in transitions.items() if s in reachable}
