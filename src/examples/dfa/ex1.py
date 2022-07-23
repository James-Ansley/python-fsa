"""
Recognises the language of words over the alphabet {0, .., 9}
which are divisible by 5 (end in 0 or 5 or are empty)

Taken from: https://www.bookofproofs.org/branches/examples-of-dfa/
"""
from dfa import DFA

a, b = "a", "b"

dfa = DFA(
    alphabet=frozenset((1, 2, 3, 4, 5, 6, 7, 8, 9, 0)),
    states=frozenset((a, b)),
    initial=a,
    transition={
        (a, 0): a, (a, 1): b, (a, 2): b, (a, 3): b, (a, 4): b, (a, 5): a,
        (a, 6): b, (a, 7): b, (a, 8): b, (a, 9): b,
        (b, 0): a, (b, 1): b, (b, 2): b, (b, 3): b, (b, 4): b, (b, 5): a,
        (b, 6): b, (b, 7): b, (b, 8): b, (b, 9): b,
    },
    final_states=frozenset((a,))
)
