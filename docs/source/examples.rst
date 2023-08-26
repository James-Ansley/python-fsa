Examples
========

DFAs
----

Example 1
^^^^^^^^^

Recognises the language of words over the alphabet {0, .., 9}
which are divisible by 5 (end in 0 or 5 or are empty)

Taken from: https://www.bookofproofs.org/branches/examples-of-dfa/

::

    from python_fsa.dfa import DFA

    a, b = "a", "b"

    dfa = DFA(
        alphabet=(1, 2, 3, 4, 5, 6, 7, 8, 9, 0),
        states=(a, b),
        initial=a,
        transitions={
            (a, 0): a, (a, 1): b, (a, 2): b, (a, 3): b, (a, 4): b, (a, 5): a,
            (a, 6): b, (a, 7): b, (a, 8): b, (a, 9): b,
            (b, 0): a, (b, 1): b, (b, 2): b, (b, 3): b, (b, 4): b, (b, 5): a,
            (b, 6): b, (b, 7): b, (b, 8): b, (b, 9): b,
        },
        final=(a,),
    )


Example 2
^^^^^^^^^

Recognises the language of words over the alphabet {0, 1}
which contain exactly two 1s

Taken from: https://www.bookofproofs.org/branches/examples-of-dfa/

::

    from python_fsa.dfa import DFA

    a, b, c, d = "a", "b", "c", "d"

    dfa = DFA(
        alphabet=frozenset((0, 1)),
        states=frozenset((a, b, c, d)),
        initial=a,
        transitions={
            (a, 0): a,
            (a, 1): b,
            (b, 0): b,
            (b, 1): c,
            (c, 0): c,
            (c, 1): d,
            (d, 0): d,
            (d, 1): d,
        },
        final=frozenset((c,))
    )


Example 3
^^^^^^^^^

Recognises the language of words over the alphabet {0, 1}
which contain an even number of 1s

Taken from: https://www.bookofproofs.org/branches/examples-of-dfa/

::

    from python_fsa.dfa import DFA

    a, b = "a", "b"

    dfa = DFA(
        alphabet=frozenset((0, 1)),
        states=frozenset((a, b)),
        initial=a,
        transitions={
            (a, 0): a,
            (a, 1): b,
            (b, 0): b,
            (b, 1): a,
        },
        final=frozenset((a,))
    )

NFAs
----

Example 1
^^^^^^^^^

Recognises the language of words over the alphabet {0, 1}
which consist of an even number of 1s or 0s

Taken from: https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton#Example_2

::

    from python_fsa.nfa import NFA

    s0, s1, s2, s3, s4 = "s0", "s1", "s2", "s3", "s4"
    E = NFA.EPSILON

    nfa = NFA(
        alphabet=frozenset((1, 0)),
        states=frozenset((s0, s1, s2, s3, s4)),
        initial=s0,
        transitions={
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
        final=frozenset((s1, s3,)),
    )

Example 2
^^^^^^^^^

Recognises the language of words over the alphabet {0, 1}
whose second to last symbol is 1.

Taken from: https://www.bookofproofs.org/branches/examples-of-nfa/

::

    from python_fsa.nfa import NFA

    a, b, c = "a", "b", "c"

    nfa = NFA(
        alphabet=frozenset((1, 0)),
        states=frozenset((a, b, c)),
        initial=a,
        transitions={
            (a, 0): frozenset((a,)),
            (a, 1): frozenset((a, b)),
            (b, 0): frozenset((c,)),
            (b, 1): frozenset((c,)),
        },
        final=frozenset((c,)),
    )


Example 3
^^^^^^^^^

Recognises the language of words over the alphabet {0, 1}
which are any combinations of the strings 10 and 101

Taken from: https://www.bookofproofs.org/branches/examples-of-nfa/

::

    from python_fsa.nfa import NFA

    a, b, c = "a", "b", "c"

    nfa = NFA(
        alphabet=frozenset((1, 0)),
        states=frozenset((a, b, c)),
        initial=a,
        transitions={
            (a, 1): frozenset((b,)),
            (b, 0): frozenset((a, c)),
            (c, 1): frozenset((a,)),
        },
        final=frozenset((a,)),
    )
