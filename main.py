from python_fsa.dfa import DFA

a, b = "a", "b"

dfa = DFA(
    alphabet=(0, 1),
    states=(a, b),
    initial=a,
    transitions={(a, 0): a, (a, 1): b, (b, 0): b, (b, 1): a},
    final=(a,),
)

dfa.accepts((1, 0, 1, 0))  # True
dfa.accepts((1, 1, 1, 0))  # False

from python_fsa.nfa import NFA

s0, s1, s2, s3, s4 = "s0", "s1", "s2", "s3", "s4"
E = NFA.EPSILON

nfa = NFA(
    alphabet=(1, 0),
    states=(s0, s1, s2, s3, s4),
    initial=s0,
    transitions={
        (s0, E): (s1, s3),
        (s1, 0): (s2,),
        (s1, 1): (s1,),
        (s2, 0): (s1,),
        (s2, 1): (s2,),
        (s3, 0): (s3,),
        (s3, 1): (s4,),
        (s4, 0): (s4,),
        (s4, 1): (s3,),
    },
    final=(s1, s3),
)

nfa.accepts((1, 0, 1))  # True
nfa.accepts((1, 0))  # False

from python_fsa.graph import dfa_from_dot, nfa_from_dot, render, to_dot

# FSA to Graphviz dot code
nfa_dot = to_dot(nfa)
dfa_dot = to_dot(dfa)

# Graphviz dot code to FSA
new_nfa = nfa_from_dot(nfa_dot)
new_dfa = dfa_from_dot(dfa_dot)

# Render FSA as Graphviz diagram
render(nfa, "docs/source/assets/nfa_example.svg")
render(dfa, "docs/source/assets/dfa_example.svg")
