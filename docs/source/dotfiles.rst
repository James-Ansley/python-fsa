Graphviz Dot Files
==================

FSAs can be parsed from strings representing graphviz digraphs.
For example:

::

    dot = r"""
    digraph {
        rankdir = LR;
        null [label = " ",shape = none,height = 0,width = 0];
        {null rank = "min"};
        node [shape = doublecircle]; C;
        node [shape = circle];
        null -> A;
        A -> A [label = "0, 1"];
        A -> B [label = "1"];
        B -> C [label = "0, 1"];
    }
    """

    nfa = NFA.from_dot(dot)


Dot files can be parsed into FSMs provided they satisfy the following
conditions:

- Has one node with the name "null" with a single edge to the initial state this
  can be made to be invisible by
  prepending ``null [label=" ",shape=none,height=0,width=0];`` to your
  graph. (optionally, add ``{null rank="min"};`` as well to force this edge to
  appear on the left)
- Final states have shape "doublecircle"
- Multiple transitions using the same edge must separate alphabet symbols by
  commas.