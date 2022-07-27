"""
Recognises the language of words over the alphabet {0, 1}
which contain exactly two 1s

Taken from: https://www.bookofproofs.org/branches/examples-of-dfa/
"""
from python_fsa.dfa import DFA

a, b, c, d = "a", "b", "c", "d"

dfa = DFA(
    alphabet=frozenset((0, 1)),
    states=frozenset((a, b, c, d)),
    initial=a,
    transition={
        (a, 0): a,
        (a, 1): b,
        (b, 0): b,
        (b, 1): c,
        (c, 0): c,
        (c, 1): d,
        (d, 0): d,
        (d, 1): d,
    },
    final_states=frozenset((c,))
)
