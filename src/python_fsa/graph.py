"""
Several utility functions to convert FSAs to and from dot graph format,
and render FSAs as dot graphs.
"""

from collections import defaultdict
from collections.abc import Iterator
from pathlib import PurePath
from textwrap import dedent, indent

try:
    from pygraphviz import AGraph
except ImportError:
    AGraph = None

from .dfa import DFA
from .nfa import NFA

__all__ = ["to_dot", "nfa_from_dot", "dfa_from_dot", "render"]


def to_dot(fsa: DFA | NFA) -> str:
    """Converts the given FSA to a graphviz dot graph"""
    if isinstance(fsa, DFA):
        return _format_dfa(fsa)
    elif isinstance(fsa, NFA):
        return _format_nfa(fsa)
    else:
        raise ValueError("fsa is not instance of DFA or NFA")


def nfa_from_dot(dot: str, epsilon=NFA.EPSILON) -> NFA:
    """Converts a NFA graphviz dot graph to an NFA object"""
    _check_graphviz()
    g = AGraph(dot)
    edges, nodes = g.edges(), g.nodes()

    transitions = defaultdict(set)
    for edge in edges:
        s, s1 = edge
        labels = edge.attr["label"]
        if s != "null":
            for label in labels.split(", "):
                transitions[(s, label)].add(s1)

    alphabet = (
        l for e in edges for l in e.attr["label"].split(", ")
        if e.attr["label"] not in [epsilon, ""]
    )
    return NFA(
        alphabet=alphabet,
        states=(str(n) for n in nodes if n != "null"),
        initial=next(e[1] for e in edges if e[0] == "null"),
        transitions=transitions,
        final=(str(n) for n in nodes if n.attr["shape"] == "doublecircle"),
        epsilon=epsilon,
    )


def dfa_from_dot(dot: str) -> DFA:
    """Converts a DFA graphviz dot graph to a DFA object"""
    _check_graphviz()
    g = AGraph(dot)
    edges, nodes = g.edges(), g.nodes()
    return DFA(
        alphabet=(e.attr["label"] for e in edges),
        states=(str(n) for n in nodes if n != "null"),
        initial=next(e[1] for e in edges if e[0] == "null"),
        transitions={
            (e[0], e.attr["label"]): e[1] for e in edges if e[0] != "null"
        },
        final=(str(n) for n in nodes if n.attr["shape"] == "doublecircle"),
    )


def render(fsa: DFA | NFA, path: str | PurePath, renderer: str = "dot") -> None:
    """Writes the given FSA to an image file at the given path"""
    AGraph(to_dot(fsa)).draw(path, prog=renderer)


def _format_dfa(dfa: "DFA") -> str:
    transitions = _melt_dfa(dfa.transitions)
    return _graph(transitions, dfa.initial, dfa.final)


def _format_nfa(nfa: "NFA") -> str:
    transitions = _melt_nfa(nfa.transitions)
    return _graph(transitions, nfa.initial, nfa.final)


def _edges(edge_map) -> Iterator[str]:
    for (from_, to), label in edge_map.items():
        yield f"""{from_} -> {to} [label = "{label}"];"""


def _graph(transition, initial, final):
    graph_edges = "\n".join(_edges(transition))
    final = " ".join(str(s) for s in final)
    return dedent(
        f"""
        digraph {{
            rankdir = LR;
            null [label = " ", shape = none, height = 0, width = 0];
            {{null rank = "min"}};
            node [shape = doublecircle]; {final};
            node [shape = circle];
            null -> {initial};
            {indent(graph_edges, ' ' * 12).lstrip()}
        }}
        """.strip("\n")
    )


def _melt_nfa(transitions):
    melted = defaultdict(list)
    for (from_, label), to_states in transitions.items():
        for to in to_states:
            melted[(from_, to)].append(str(label))
    return {(from_, to): ", ".join(labels)
            for (from_, to), labels in melted.items()}


def _melt_dfa(transitions):
    melted = defaultdict(list)
    for (from_, label), to in transitions.items():
        melted[(from_, to)].append(str(label))
    return {(from_, to): ", ".join(labels)
            for (from_, to), labels in melted.items()}


def _check_graphviz():
    if AGraph is None:
        raise ModuleNotFoundError(
            "Cannot load the pygraphviz module to render fsa, "
            "try reinstalling python-fsa with the graphviz option."
        )
