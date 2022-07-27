"""
Recognises the language of words over the alphabet {0, 1}
which consist of an even number of 1s or 0s

Taken from:
    https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton#Example_2
"""

from python_fsa.nfa import NFA

s0, s1, s2, s3, s4 = "s0", "s1", "s2", "s3", "s4"
E = NFA.epsilon

nfa = NFA(
    alphabet=frozenset((1, 0)),
    states=frozenset((s0, s1, s2, s3, s4)),
    initial=s0,
    transition={
        (s0, E): frozenset((s1, s3)),
        (s1, 0): frozenset((s2,)),
        (s1, 1): frozenset((s1,)),
        (s2, 0): frozenset((s1,)),
        (s2, 1): frozenset((s2,)),
        (s3, 0): frozenset((s3,)),
        (s3, 1): frozenset((s4,)),
        (s4, 0): frozenset((s4,)),
        (s4, 1): frozenset((s3,)),
    },
    final_states=frozenset((s1, s3,)),
)
