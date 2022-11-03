from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_fsa import DFA, NFA

# TODO – Should probably do this properly with pygraphviz
TEMPLATE = """digraph {{
    rankdir = LR;
    null [label = " ",shape = none,height = 0,width = 0];
    {{null rank = "min"}};
    node [shape = doublecircle]; {final};
    node [shape = circle];
    null -> {initial};
{edges}
}}"""

EDGE_TEMPLATE = """    {from_} -> {to} [label = "{with_}"];"""


def squash_dfa_transitions(transitions):
    compact_transitions = defaultdict(list)
    for (from_, with_), to in transitions.items():
        compact_transitions[(from_, to)].append(with_)
    return {k: ", ".join(str(s) for s in v)
            for k, v in compact_transitions.items()}


def squash_nfa_transitions(transitions):
    compact_transitions = defaultdict(list)
    for (from_, with_), to in transitions.items():
        for to1 in to:
            compact_transitions[(from_, to1)].append(with_)
    return {k: ", ".join(str(s) for s in v)
            for k, v in compact_transitions.items()}


def format_edges(transitions):
    return [
        EDGE_TEMPLATE.format(from_=from_, with_=with_, to=to)
        for (from_, to), with_ in transitions.items()
    ]


def format_dfa(dfa: "DFA") -> str:
    transitions = squash_dfa_transitions(dfa.transition)
    edges = format_edges(transitions)
    return TEMPLATE.format(
        initial=dfa.initial,
        final=" ".join(str(s) for s in dfa.final_states),
        edges="\n".join(edges),
    )


def format_nfa(nfa: "NFA") -> str:
    transitions = squash_nfa_transitions(nfa.transition)
    edges = format_edges(transitions)
    initial = nfa.initial
    return TEMPLATE.format(
        initial=initial,
        final=" ".join(str(s) for s in nfa.final_states),
        edges="\n".join(edges),
    )
