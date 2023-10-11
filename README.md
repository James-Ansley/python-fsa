# Finite State Automata

A small project demonstrating both deterministic and nondeterministic finite
state machines.

![](assets/meme.png)

## Docs

https://python-fsa.rtfd.io/

## Install

```
pip install python-fsa
```

Python-fsa depends on graphviz and pygraphviz. In order to install graphviz,
see [their documentation](https://github.com/pygraphviz/pygraphviz/blob/main/INSTALL.txt)

## Examples

### DFA Example

Consider the following DFA that recognises the language of words over the
alphabet {0, 1} which contain an even number of 1s

![](assets/dfa_example.svg)

A DFA instance can be constructed:

```python
from python_fsa.dfa import DFA

a, b = "a", "b"

dfa = DFA(
    alphabet=(0, 1),
    states=(a, b),
    initial=a,
    transitions={
        (a, 0): a,
        (a, 1): b,
        (b, 0): b,
        (b, 1): a,
    },
    final=(a,),
)
```

Words can then be accepted or rejected by calling `accepts`:

```python
dfa.accepts((0, 0, 0, 1))  # False
dfa.accepts((0, 1, 1, 0))  # True
```

Words can be given one at a time to a mutable transducer of the DFA:

```python
dfa_transducer = dfa.transducer()

dfa_transducer.push(1)  # False
dfa_transducer.push(0)  # False
dfa_transducer.push(1)  # True
dfa_transducer.push(0)  # True
```

### NFA Example

Consider the following NFA that recognises the language of words over the
alphabet {0, 1} whose second to last symbol is 1.

![](assets/nfa_example.svg)

An NFA instance can be constructed:

```python
from python_fsa.nfa import NFA

a, b, c = "a", "b", "c"

nfa = NFA(
    alphabet=(1, 0),
    states=(a, b, c),
    initial=a,
    transitions={
        (a, 0): (a,),
        (a, 1): (a, b),
        (b, 0): (c,),
        (b, 1): (c,),
    },
    final=(c,),
)
```

Words can then be accepted or rejected by calling `accepts`:

```python
nfa.accepts((0, 1, 1, 0))  # True
nfa.accepts((0, 0, 0, 1))  # False
```

This NFA can be converted to an equivalent DFA by calling `to_dfa`:

```python
dfa = nfa.to_dfa()
```

However, this will result in a DFA of type `DFA[T, frozenset[S]]` – as the
states of the resulting DFA are from the powerset of NFA states. This can cause
errors in writing the resulting DFA to dot-format.

The `frozenset[S]` states can be squashed to strings by calling `dfa.squash()`,
which stringifies and joins states in each `frozenset[S]`:

```python
dfa = nfa.to_dfa().squash()
```

Which produces the following DFA:

![](assets/nfa_to_dfa_ex.svg)
