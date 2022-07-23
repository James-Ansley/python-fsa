"""
Recognises the language of words over the alphabet {0, 1}
which contain an even number of 1s

Taken from: https://www.bookofproofs.org/branches/examples-of-dfa/
"""
from dfa import DFA

a, b = "a", "b"

dfa = DFA(
    alphabet=frozenset((0, 1)),
    states=frozenset((a, b)),
    initial=a,
    transition={
        (a, 0): a,
        (a, 1): b,
        (b, 0): b,
        (b, 1): a,
    },
    final_states=frozenset((a,))
)
