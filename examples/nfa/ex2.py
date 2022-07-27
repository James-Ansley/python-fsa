"""
Recognises the language of words over the alphabet {0, 1}
whose second to last symbol is 1.

Taken from: https://www.bookofproofs.org/branches/examples-of-nfa/
"""

from python_fsa.nfa import NFA

a, b, c = "a", "b", "c"

nfa = NFA(
    alphabet=frozenset((1, 0)),
    states=frozenset((a, b, c)),
    initial=a,
    transition={
        (a, 0): frozenset((a,)),
        (a, 1): frozenset((a, b)),
        (b, 0): frozenset((c,)),
        (b, 1): frozenset((c,)),
    },
    final_states=frozenset((c,)),
)
