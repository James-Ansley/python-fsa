"""
A deterministic finite state machine and its corresponding transducer
"""

from collections.abc import Hashable, Iterable, Mapping
from pprint import pformat
from textwrap import indent
from typing import Final, Generic, TypeVar

__all__ = ["DFA", "DFATransducer"]

T = TypeVar("T", bound=Hashable)
S = TypeVar("S", bound=Hashable)
V = TypeVar("V")
Alphabet = frozenset[T]
States = frozenset[S]
Transitions = Mapping[tuple[S, T], S]


class DFA(Generic[T, S]):
    """
    A deterministic finite state machine.

    Allows for transitions to be a partial function – in the case a
    transition is not defined, the state becomes None.

    DFAs are immutable and can only accept or reject whole sequences of tokens.
    However, a mutable DFATransducer can be constructed with the
    :meth:`transducer` method which can accept one token at a time.
    """

    def __init__(
          self,
          *,
          alphabet: Iterable[T],
          states: Iterable[S],
          initial: S,
          transitions: Transitions,
          final: Iterable[S],
    ):
        self.alphabet: Final[Alphabet] = frozenset(alphabet)
        self.states: Final[States] = frozenset(states)
        self.initial: Final[S] = initial
        self.transitions: Final[Transitions] = dict(transitions)
        self.final: Final[States] = frozenset(final)

    def accepts(self, input: Iterable[T]) -> bool:
        """
        Returns True if the given input is accepted by this DFA and
        False otherwise
        """
        current = self.initial
        for e in input:
            current = self.transitions.get((current, e), None)
        return current in self.final

    def transducer(
          self, output: Mapping[S, V] = None) -> "DFATransducer[T, S, V]":
        """
        Returns a transducer with the given output mapping. By default,
        this maps states to a boolean indicating whether that state is an
        accepting/final state.
        """
        if output is None:
            output = {s: s in self.final for s in self.states}
        return DFATransducer(self, output)

    def squash(self) -> "DFA[T, str]":
        """
        Converts all states to strings – any non-string iterables are joined
        to a string in sorted alphabetical order.

        This is useful when wanting to render the DFA as graph.
        """
        return DFA(
            alphabet=self.alphabet,
            states=(_join(state) for state in self.states),
            initial=_join(self.initial),
            transitions={
                (_join(from_), t): _join(to)
                for (from_, t), to in self.transitions.items()
            },
            final=(_join(state) for state in self.final),
        )

    def __str__(self):
        return "\n".join((
            "DFA(",
            indent(f"alphabet={pformat(self.alphabet)},", " " * 4),
            indent(f"states={pformat(self.states)},", " " * 4),
            indent(f"initial={pformat(self.initial)},", " " * 4),
            indent(f"transitions={pformat(self.transitions)}", " " * 4),
            indent(f"final={pformat(self.final)},", " " * 4),
            ")",
        ))


class DFATransducer(Generic[T, S, V]):
    """
    A mutable Moore machine that accepts inputs one at a time.

    Allows for the DFA transitions to be a partial function – in the case a
    transition is not defined, the state and output become None, unless None
    is in the output domain.
    """

    def __init__(self, dfa: DFA[T, S], output: Mapping[S, V]):
        self._dfa = dfa
        self._output = output
        self._current = dfa.initial

    @property
    def current(self) -> S:
        """The current state of the transducer"""
        return self._current

    @property
    def output(self) -> V:
        """The current output of the transducer"""
        return self._output.get(self._current, None)

    @property
    def is_accepting(self) -> bool:
        """Returns True if the transducer is in an accepting state"""
        return self._current in self._dfa.final

    def push(self, input: T) -> V:
        """Transitions the transducer and returns the new output"""
        current = self._current
        self._current = self._dfa.transitions.get((current, input), None)
        return self.output


def _join(elts):
    if isinstance(elts, str):
        return elts
    elif isinstance(elts, Iterable):
        return "".join(sorted(str(e) for e in elts))
    else:
        return str(elts)
