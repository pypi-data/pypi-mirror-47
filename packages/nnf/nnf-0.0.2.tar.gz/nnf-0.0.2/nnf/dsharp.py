"""A parser for DSHARP's output format.

Derived by closely studying its output and source code. This format might
be some sort of established standard, in which case this parser might reject
some valid files in the format.
"""

import io
import typing as t

from nnf import NNF, And, Or, Var


def load(fp: t.TextIO) -> NNF:
    fmt, nodecount, edges, varcount = fp.readline().split()
    node_specs = dict(enumerate(line.split() for line in fp))
    assert fmt == 'nnf'
    nodes: t.Dict[int, NNF] = {}
    for num, spec in node_specs.items():
        if spec[0] == 'L':
            if spec[1].startswith('-'):
                nodes[num] = Var(int(spec[1][1:]), False)
            else:
                nodes[num] = Var(int(spec[1]))
        elif spec[0] == 'A':
            nodes[num] = And(nodes[int(n)] for n in spec[2:])
        elif spec[0] == 'O':
            nodes[num] = Or(nodes[int(n)] for n in spec[3:])
        else:
            raise ValueError(f"Can't parse line {num}: {spec}")
    return nodes[int(nodecount) - 1]


def loads(s: str) -> NNF:
    return load(io.StringIO(s))
