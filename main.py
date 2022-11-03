from python_fsa import EPSILON
from python_fsa.nfa import NFA


s0, s1, s2, s3, s4 = "s0", "s1", "s2", "s3", "s4"
E = EPSILON

nfa = NFA.from_dot("""
digraph {
    rankdir = LR;
    null [label = " ",shape = none,height = 0,width = 0];
    {null rank = "min"};
    node [shape = doublecircle]; s1 s3 s0;
    node [shape = circle];
    null -> s0;
    s0 -> s1 [label = "ε"];
    s0 -> s3 [label = "ε"];
    s1 -> s2 [label = "0"];
    s1 -> s1 [label = "1"];
    s2 -> s1 [label = "0"];
    s2 -> s2 [label = "1"];
    s3 -> s3 [label = "0"];
    s3 -> s4 [label = "1"];
    s4 -> s4 [label = "0"];
    s4 -> s3 [label = "1"];
}
""")

dfa = nfa.to_dfa()
dfa = dfa.squash()

print(nfa.to_dot())
