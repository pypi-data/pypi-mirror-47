"""A parser and serializer for the DIMACS CNF and SAT formats.

https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html
"""

import collections
import io
import typing as t
import warnings

from nnf import NNF, Var, And, Or, Name, true, false

# TODO: cnf format


def dump(
        obj: NNF,
        fp: t.TextIO,
        *,
        num_variables: t.Optional[int] = None,
        var_labels: t.Optional[t.Dict[Name, int]] = None,
        comment_header: t.Optional[str] = None,
        mode: str = 'sat'
) -> None:
    num_vars: int
    if num_variables is None:
        if var_labels is None:
            names: t.FrozenSet[int] = obj.vars()  # type: ignore
            for name in names:
                if not isinstance(name, int) or name <= 0:
                    raise TypeError(
                        f"{name!r} is not an integer > 0. Try supplying a "
                        "var_labels dictionary."
                    )
            num_vars = max(names, default=0)
        else:
            num_vars = max(var_labels.values(), default=0)
    else:
        num_vars = num_variables

    if mode == 'sat':
        _dump_sat(obj, fp, num_variables=num_vars, var_labels=var_labels,
                  comment_header=comment_header)
    elif mode == 'cnf':
        _dump_cnf(obj, fp, num_variables=num_vars, var_labels=var_labels,
                  comment_header=comment_header)


def _write_comments(comment_header: str, fp: t.TextIO) -> None:
    for line in comment_header.split('\n'):
        fp.write('c ')
        fp.write(line)
        fp.write('\n')


def _format_var(
        node: Var,
        num_variables: int,
        var_labels: t.Optional[t.Dict[Name, int]] = None
) -> str:
    if var_labels is not None:
        name = var_labels[node.name]
    else:
        name = node.name  # type: ignore
    if not isinstance(name, int) or name <= 0:
        raise TypeError(f"{name!r} is not an integer > 0")
    if name > num_variables:
        raise ValueError(
            f"{name!r} is more than num_variables"
        )
    if not node.true:
        return f"-{name}"
    return str(name)


def _dump_sat(
        obj: NNF,
        fp: t.TextIO,
        *,
        num_variables: int,
        var_labels: t.Optional[t.Dict[Name, int]] = None,
        comment_header: t.Optional[str] = None,
) -> None:
    if comment_header is not None:
        _write_comments(comment_header, fp)

    fp.write(f"p sat {num_variables}\n")

    def serialize(node: NNF) -> None:
        if isinstance(node, Var):
            fp.write(_format_var(node, num_variables, var_labels))
        elif isinstance(node, (Or, And)):
            fp.write('+(' if isinstance(node, Or) else '*(')
            first = True
            for child in node.children:
                if first:
                    first = False
                else:
                    fp.write(' ')
                serialize(child)
            fp.write(')')
        else:
            raise TypeError(f"Can't serialize type {type(node)}")

    fp.write('(')
    serialize(obj)
    fp.write(')')


def _dump_cnf(
        obj: NNF,
        fp: t.TextIO,
        *,
        num_variables: int,
        var_labels: t.Optional[t.Dict[Name, int]] = None,
        comment_header: t.Optional[str] = None,
) -> None:
    if not isinstance(obj, And):
        raise TypeError("CNF sentences must be conjunctions")

    if comment_header is not None:
        _write_comments(comment_header, fp)

    fp.write(f"p cnf {num_variables} {len(obj.children)}\n")

    first = True
    for clause in obj.children:
        if not isinstance(clause, Or):
            raise TypeError("CNF sentences must be conjunctions of "
                            "disjunctions")
        if not len(clause.children) > 0:
            raise TypeError("CNF sentences shouldn't have empty clauses")
        if not first:
            fp.write('0')
        else:
            first = False
        for child in clause.children:
            if not isinstance(child, Var):
                raise TypeError("CNF sentences must be conjunctions of "
                                "disjunctions of variables")
            fp.write(' ')
            fp.write(_format_var(child, num_variables, var_labels))
        fp.write('\n')


def dumps(
        obj: NNF,
        *,
        num_variables: t.Optional[int] = None,
        var_labels: t.Optional[t.Dict[Name, int]] = None,
        comment_header: t.Optional[str] = None,
        mode: str = 'sat'
) -> str:
    buffer = io.StringIO()
    dump(obj, buffer, num_variables=num_variables, var_labels=var_labels,
         comment_header=comment_header, mode=mode)
    return buffer.getvalue()


def load(fp: t.TextIO) -> NNF:
    for line in fp:
        if line.startswith('c'):
            continue
        if line.startswith('p '):
            problem = line.split()
            if len(line) < 2:
                raise ValueError("Malformed problem line")
            fmt = problem[1]
            if 'sat' in fmt or 'SAT' in fmt:
                # problem[2] contains the number of variables
                # but that's currently not explicitly represented
                return _load_sat(fp)
            elif 'cnf' in fmt or 'CNF' in fmt:
                # problem[2] has the number of variables
                # problem[3] has the number of clauses
                return _load_cnf(fp)
            else:
                raise ValueError(f"Unknown format '{fmt}'")
        else:
            print(repr(line))
            raise ValueError(
                "Couldn't find a problem line before an unknown kind of line"
            )
    else:
        raise ValueError(
            "Couldn't find a problem line before the end of the file"
        )


def loads(s: str) -> NNF:
    return load(io.StringIO(s))


def _load_sat(fp: t.TextIO) -> NNF:
    tokens: t.Deque[str] = collections.deque()
    for line in fp:
        if line.startswith('c'):
            continue
        tokens.extend(
            line.replace('(', '( ')
                .replace(')', ' ) ')
                .replace('+(', ' +(')
                .replace('*(', ' *(')
                .replace('-', ' - ')
                .split()
        )
    result = _parse_sat(tokens)
    if tokens:
        warnings.warn("Found extra tokens past the end of the sentence")
    return result


def _parse_sat(tokens: t.Deque[str]) -> NNF:
    cur = tokens.popleft()
    if cur == '(':
        content = _parse_sat(tokens)
        close = tokens.popleft()
        if close != ')':
            raise ValueError(f"Expected closing paren, found {close!r}")
        return content
    elif cur == '-':
        content = _parse_sat(tokens)
        if not isinstance(content, Var):
            raise ValueError(f"Only variables can be negated, not {content!r}")
        return ~content
    elif cur == '*(':
        children = []
        while tokens[0] != ')':
            children.append(_parse_sat(tokens))
        tokens.popleft()
        if children:
            return And(children)
        else:
            return true
    elif cur == '+(':
        children = []
        while tokens[0] != ')':
            children.append(_parse_sat(tokens))
        tokens.popleft()
        if children:
            return Or(children)
        else:
            return false
    elif cur.isdigit():
        return Var(int(cur))
    else:
        raise ValueError(f"Found unexpected token {cur!r}")


def _load_cnf(fp: t.TextIO) -> NNF:
    tokens: t.Deque[str] = collections.deque()
    for line in fp:
        if line.startswith('c'):
            continue
        tokens.extend(
            line.replace('-', ' -')
                .split()
        )
    return _parse_cnf(tokens)


def _parse_cnf(tokens: t.Deque[str]) -> NNF:
    clauses: t.Set[Or] = set()
    clause: t.Set[Var] = set()
    for token in tokens:
        if token == '0':
            if clause:
                clauses.add(Or(clause))
            clause = set()
        elif token == '%':
            # Some example files end with:
            # 0
            # %
            # 0
            # I don't know why.
            pass
        elif token.startswith('-'):
            clause.add(Var(int(token[1:]), False))
        else:
            clause.add(Var(int(token)))
    if clause:
        # A file may or may not end with a 0
        # Adding an empty clause is not desirable
        clauses.add(Or(clause))
    return And(clauses)
