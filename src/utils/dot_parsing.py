import re
from collections import defaultdict
from collections.abc import Mapping

import sentinel
from pygraphviz import AGraph

EPSILON_STRING = "\u03B5"
EPSILON = sentinel.create("epsilon")

__all__ = [
    "alphabet_of",
    "states_of",
    "finial_states_of",
    "initial_state_of",
    "deterministic_transitions_of",
    "nondeterministic_transitions_of",
]


def split_label(label: str):
    return re.split(r",\s*", label)


def alphabet_of(g: AGraph) -> frozenset[str]:
    alphabet = set()
    for edge in g.edges():
        s = edge[0].name
        if s != "null":
            alphabet = alphabet.union(
                EPSILON if label == EPSILON_STRING else label
                for label in split_label(edge.attr["label"])
            )
    return frozenset(alphabet)


def states_of(g: AGraph) -> frozenset[str]:
    return frozenset(n.name for n in g.nodes() if n.name != "null")


def finial_states_of(g: AGraph) -> frozenset[str]:
    return frozenset(
        n.name for n in g.nodes() if n.attr["shape"] == "doublecircle"
    )


def initial_state_of(g: AGraph) -> str:
    return g.edges("null")[0][1].name


def deterministic_transitions_of(g: AGraph) -> Mapping[tuple[str, str], str]:
    transition = {}
    for edge in g.edges():
        s, s1 = edge[0].name, edge[1].name
        labels = split_label(edge.attr["label"])
        if s != "null":
            for label in labels:
                transition[(s, label)] = s1
    return transition


def nondeterministic_transitions_of(
        g: AGraph
) -> Mapping[tuple[str, str], frozenset[str]]:
    transition = defaultdict(set)
    for edge in g.edges():
        s, s1 = edge[0].name, edge[1].name
        labels = split_label(edge.attr["label"])
        if s != "null":
            for label in labels:
                transition[(s, label)].add(s1)
    return {k: frozenset(v) for k, v in transition.items()}
