"""
Recognises the language of words over the alphabet {0, 1}
which are any combinations of the strings 10 and 101

Taken from: https://www.bookofproofs.org/branches/examples-of-nfa/
"""

from nfa import NFA

a, b, c = "a", "b", "c"

nfa = NFA(
    alphabet=frozenset((1, 0)),
    states=frozenset((a, b, c)),
    initial=a,
    transition={
        (a, 1): frozenset((b,)),
        (b, 0): frozenset((a, c)),
        (c, 1): frozenset((a,)),
    },
    final_states=frozenset((a,)),
)
