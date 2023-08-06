# Copyright 2018 Jan Verbeek <jan.verbeek@posteo.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import functools
import itertools
import typing as t

import nnf

Name = t.Hashable
Model = t.Dict[Name, bool]

memoize = functools.lru_cache(maxsize=None)

__all__ = ('NNF', 'Internal', 'And', 'Or', 'Var', 'Builder', 'all_models',
           'decision', 'true', 'false', 'dsharp', 'dimacs', 'amc')


def all_models(names: t.Collection[Name]) -> t.Iterator[Model]:
    """Yield dictionaries with all possible boolean values for the names.

    >>> list(all_models(["a", "b"]))
    [{'a': True, 'b': True}, {'a': False, 'b': True}, ...
    """
    if not names:
        yield {}
    else:
        name, *rest = names
        for model in all_models(rest):
            yield {name: True, **model}
            yield {name: False, **model}


T = t.TypeVar('T')
_Tristate = t.Optional[bool]


class NNF:
    """Base class for all NNF sentences."""

    def __and__(self, other: 'NNF') -> 'NNF':
        """And({self, other})"""
        return And({self, other})

    def __or__(self, other: 'NNF') -> 'NNF':
        """Or({self, other})"""
        return Or({self, other})

    def walk(self) -> t.Iterator['NNF']:
        """Yield all nodes in the sentence, depth-first.

        Nodes that appear multiple times are yielded only once.
        """
        # Could be made width-first by using a deque and popping from the left
        seen = {self}
        nodes = [self]
        while nodes:
            node = nodes.pop()
            yield node
            if isinstance(node, Internal):
                for child in node.children:
                    if child not in seen:
                        seen.add(child)
                        nodes.append(child)

    def size(self) -> int:
        """The number of edges in the sentence.

        Note that sentences are rooted DAGs, not trees. If a node has
        multiple parents its edges will still be counted just once.
        """
        return sum(len(node.children)
                   for node in self.walk()
                   if isinstance(node, Internal))

    def height(self) -> int:
        """The number of edges between here and the furthest leaf."""
        @memoize
        def height(node: NNF) -> int:
            if isinstance(node, Internal) and node.children:
                return 1 + max(height(child) for child in node.children)
            return 0

        return height(self)

    def leaf(self) -> bool:
        """True if the node doesn't have children."""
        return True

    def flat(self) -> bool:
        """A sentence is flat if its height is at most 2.

        That is, there are at most two layers below the root node.
        """
        # Could be sped up by returning as soon as a path longer than 2 is
        # found, instead of computing the full height
        return self.height() <= 2

    def simply_disjunct(self) -> bool:
        """The children of Or nodes are leaves that don't share variables."""
        return all(node.is_simple()
                   for node in self.walk()
                   if isinstance(node, Or))

    def simply_conjunct(self) -> bool:
        """The children of And nodes are leaves that don't share variables."""
        return all(node.is_simple()
                   for node in self.walk()
                   if isinstance(node, And))

    def vars(self) -> t.FrozenSet[Name]:
        """The names of all variables that appear in the sentence."""
        return frozenset(node.name
                         for node in self.walk()
                         if isinstance(node, Var))

    def decomposable(self) -> bool:
        """The children of each And node don't share variables, recursively."""
        @memoize
        def var(node: NNF) -> t.FrozenSet[Name]:
            return node.vars()

        for node in self.walk():
            if isinstance(node, And):
                seen: t.Set[Name] = set()
                for child in node.children:
                    for name in var(child):
                        if name in seen:
                            return False
                        seen.add(name)
        return True

    def deterministic(self) -> bool:
        """The children of each Or node contradict each other.

        May be very expensive.
        """
        for node in self.walk():
            if isinstance(node, Or):
                for a, b in itertools.combinations(node.children, 2):
                    if not a.contradicts(b):
                        return False
        return True

    def smooth(self) -> bool:
        """The children of each Or node all use the same variables."""
        for node in self.walk():
            if isinstance(node, Or) and len(node.children) > 1:
                expected = None
                for child in node.children:
                    if expected is None:
                        expected = child.vars()
                    else:
                        if child.vars() != expected:
                            return False
        return True

    def decision_node(self) -> bool:
        """The sentence is a valid binary decision diagram (BDD)."""
        return False

    def satisfied_by(self, model: Model) -> bool:
        """The given dictionary of values makes the sentence correct."""
        @memoize
        def sat(node: NNF) -> bool:
            if isinstance(node, Var):
                if node.name not in model:
                    # Note: because any and all are lazy, it's possible for
                    # this error not to occur even if a variable is missing.
                    # In such a case including the variable with any value
                    # would not affect the return value though.
                    raise ValueError(
                        f"Model does not contain variable {node.name!r}"
                    )
                return model[node.name] == node.true
            elif isinstance(node, Or):
                return any(sat(child) for child in node.children)
            elif isinstance(node, And):
                return all(sat(child) for child in node.children)
            else:
                raise TypeError(node)

        return sat(self)

    def satisfiable(self, decomposable: _Tristate = None) -> bool:
        """Some set of values exists that makes the sentence correct."""
        if not self._satisfiable_decomposable():
            return False

        if decomposable is None:
            decomposable = self.decomposable()

        if decomposable:
            # Would've been picked up already if not satisfiable
            return True

        return any(self.satisfied_by(model)
                   for model in all_models(self.vars()))

    def _satisfiable_decomposable(self) -> bool:
        """Checks satisfiability of decomposable sentences.

        If the sentence is not decomposable, it may return True even if the
        sentence is not satisfiable. But if it returns False the sentence is
        certainly not satisfiable.
        """
        @memoize
        def sat(node: NNF) -> bool:
            """Check satisfiability of DNNF."""
            if isinstance(node, Or):
                # note: if node == false this path is followed
                return any(sat(child) for child in node.children)
            elif isinstance(node, And):
                return all(sat(child) for child in node.children)
            return True

        return sat(self)

    def _consistent_with_model(self, model: Model) -> bool:
        """A combination of `condition` and `satisfiable`.

        Only works on decomposable sentences, but doesn't check for the
        property. Use with care.
        """
        @memoize
        def con(node: NNF) -> bool:
            if isinstance(node, Var):
                if node.name not in model:
                    return True
                if model[node.name] == node.true:
                    return True
                return False
            elif isinstance(node, Or):
                return any(con(child) for child in node.children)
            elif isinstance(node, And):
                return all(con(child) for child in node.children)
            else:
                raise TypeError(node)

        return con(self)

    consistent = satisfiable  # synonym

    def models(self, decomposable: _Tristate = None) -> t.Iterator[Model]:
        """Yield all dictionaries of values that make the sentence correct."""
        if decomposable is None:
            decomposable = self.decomposable()
        if decomposable:
            yield from self._models_decomposable()
        else:
            for model in all_models(self.vars()):
                if self.satisfied_by(model):
                    yield model

    def contradicts(
            self,
            other: 'NNF',
            decomposable: _Tristate = None
    ) -> bool:
        """There is no set of values that satisfies both sentences.

        May be very expensive.
        """
        if decomposable is None:
            decomposable = self.decomposable() and other.decomposable()

        if len(self.vars()) > len(other.vars()):
            # The one with the fewest vars has the smallest models
            a, b = other, self
        else:
            a, b = self, other

        if decomposable:
            for model in a.models(decomposable=True):
                if b._consistent_with_model(model):
                    return False
            return True

        for model in b.models():
            # Hopefully, a.vars() <= b.vars() and .satisfiable() is fast
            if a.condition(model).satisfiable():
                return False
        return True

    def to_MODS(self) -> 'NNF':
        """Convert the sentence to a MODS sentence."""
        return Or(And(Var(name, val)
                      for name, val in model.items())
                  for model in self.models())

    def to_model(self) -> Model:
        """If the sentence directly represents a model, convert it to that.

        A sentence directly represents a model if it's a conjunction of
        (unique) variables, or a single variable.
        """
        if isinstance(self, Var):
            return {self.name: self.true}
        if not isinstance(self, And):
            raise TypeError("A sentence can only be converted to a model if "
                            "it's a conjunction of variables.")
        model: Model = {}
        for child in self.children:
            if not isinstance(child, Var):
                raise TypeError("A sentence can only be converted to a "
                                "model if it's a conjunction of variables.")
            if child.name in model:
                raise ValueError(f"{child.name!r} appears multiple times.")
            model[child.name] = child.true

        return model

    def condition(self, model: Model) -> 'NNF':
        """Fill in all the values in the dictionary."""
        @memoize
        def cond(node: NNF) -> NNF:
            if isinstance(node, Var):
                if node.name not in model:
                    return node
                if model[node.name] == node.true:
                    return true
                return false
            elif isinstance(node, Internal):
                new = node.__class__(map(cond, node.children))
                if new != node:
                    return new
                return node
            else:
                raise TypeError(type(node))

        return cond(self)

    def simplify(self) -> 'NNF':
        """Apply the following transformations to make the sentence simpler:

        - If an And node has `false` as a child, replace it by `false`
        - If an Or node has `true` as a child, replace it by `true`
        - Remove children of And nodes that are `true`
        - Remove children of Or nodes that are `false`
        - If an And or Or node only has one child, replace it by that child
        - If an And or Or node has a child of the same type, merge them
        """
        # TODO: which properties does this preserve?

        @memoize
        def simple(node: NNF) -> NNF:
            if isinstance(node, Var):
                return node
            new_children: t.Set[NNF] = set()
            if isinstance(node, Or):
                for child in map(simple, node.children):
                    if child == true:
                        return true
                    elif child == false:
                        pass
                    elif isinstance(child, Or):
                        new_children.update(child.children)
                    else:
                        new_children.add(child)
                if len(new_children) == 0:
                    return false
                elif len(new_children) == 1:
                    return list(new_children)[0]
                return Or(new_children)
            elif isinstance(node, And):
                for child in map(simple, node.children):
                    if child == false:
                        return false
                    elif child == true:
                        pass
                    elif isinstance(child, And):
                        new_children.update(child.children)
                    else:
                        new_children.add(child)
                if len(new_children) == 0:
                    return true
                elif len(new_children) == 1:
                    return list(new_children)[0]
                return And(new_children)
            else:
                raise TypeError(node)

        return simple(self)

    def deduplicate(self) -> 'NNF':
        """Return a copy of the sentence without any duplicate objects.

        If a node has multiple parents, it's possible for it to be
        represented by two separate objects. This method gets rid of that
        duplication.

        In a lot of cases it's better to avoid the duplication in the first
        place, for example with a Builder object.
        """
        new_nodes: t.Dict[NNF, NNF] = {}

        def recreate(node: NNF) -> NNF:
            if node not in new_nodes:
                if isinstance(node, Var):
                    new_nodes[node] = node
                elif isinstance(node, Or):
                    new_nodes[node] = Or(recreate(child)
                                         for child in node.children)
                elif isinstance(node, And):
                    new_nodes[node] = And(recreate(child)
                                          for child in node.children)
            return new_nodes[node]

        return recreate(self)

    def object_count(self) -> int:
        """Return the number of distinct node objects in the sentence."""
        ids: t.Set[int] = set()

        def count(node: NNF) -> None:
            ids.add(id(node))
            if isinstance(node, Internal):
                for child in node.children:
                    if id(child) not in ids:
                        count(child)

        count(self)
        return len(ids)

    def to_DOT(self, color: bool = False) -> str:
        """Output a representation of the sentence in the DOT language.

        DOT is a graph visualization language.
        """
        # TODO: offer more knobs
        #       - add own directives
        #       - set different palette
        counter = itertools.count()
        names: t.Dict[NNF, t.Tuple[int, str, str]] = {}
        arrows: t.List[t.Tuple[int, int]] = []

        def name(node: NNF) -> int:
            if node not in names:
                number = next(counter)
                if isinstance(node, Var):
                    label = str(node.name).replace('"', r'\"')
                    color = 'chartreuse'
                    if not node.true:
                        label = '¬' + label
                        color = 'pink'
                    names[node] = (number, label, color)
                elif node == true:
                    names[node] = (number, "⊤", 'green')
                elif node == false:
                    names[node] = (number, "⊥", 'red')
                elif isinstance(node, And):
                    names[node] = (number, "∧", 'lightblue')
                elif isinstance(node, Or):
                    names[node] = (number, "∨", 'yellow')
                else:
                    raise TypeError(f"Can't handle node of type {type(node)}")
            return names[node][0]

        for node in sorted(self.walk()):
            name(node)
        for node in sorted(self.walk()):
            if isinstance(node, Internal):
                for child in sorted(node.children):
                    arrows.append((name(node), name(child)))

        return '\n'.join([
            'digraph {',
            *(
                f'    {number} [label="{label}"'
                + (f' fillcolor="{fillcolor}" style=filled]' if color else ']')
                for number, label, fillcolor in names.values()
            ),
            *(
                f'    {src} -> {dst}'
                for src, dst in arrows
            ),
            '}\n'
        ])

    def transform(
            self,
            func: t.Callable[[t.Callable[['NNF'], T], 'NNF'], T]
    ) -> T:
        """A helper function to apply a transformation with memoization.

        It should be passed a function that takes as its first argument a
        function that wraps itself, to use for recursive calls.

        For example::

            def vars(transform, node):
                if isinstance(node, Var):
                    return {node.name}
                else:
                    return {name for child in node.children
                           for name in transform(child)}

            names = sentence.transform(vars)
        """
        @memoize
        def transform(node: NNF) -> T:
            return func(transform, node)

        return transform(self)

    def models_smart(self) -> t.Iterator[Model]:
        """An alternative to .models().

        Potentially much faster if there are few models, but potentially
        much slower if there are many models.

        A pathological case is `Or({Var(1), Var(2), Var(3), ...})`.
        """
        ModelInt = t.FrozenSet[t.Tuple[Name, bool]]

        def compatible(a: ModelInt, b: ModelInt) -> bool:
            if len(a) > len(b):
                a, b = b, a
            return not any((name, not value) in b for name, value in a)

        def extract(
                transform: t.Callable[[NNF], t.Iterable[ModelInt]],
                node: NNF
        ) -> t.Set[ModelInt]:
            if isinstance(node, Var):
                return {frozenset(((node.name, node.true),))}
            elif isinstance(node, Or):
                return {model
                        for child in node.children
                        for model in transform(child)}
            elif isinstance(node, And):
                models: t.Set[ModelInt] = {frozenset()}
                for child in node.children:
                    models = {existing | new
                              for new in transform(child)
                              for existing in models
                              if compatible(existing, new)}
                return models
            raise TypeError(node)

        names = self.vars()
        full_models: t.Set[ModelInt] = set()

        def complete(
                model: ModelInt,
                names: t.List[Name]
        ) -> t.Iterator[ModelInt]:
            for expansion in all_models(names):
                yield frozenset(model | expansion.items())

        for model in self.transform(extract):
            missing_names = list(names - {name for name, value in model})
            if not missing_names:
                full_models.add(model)
            else:
                full_models.update(complete(model, missing_names))

        for full_model in full_models:
            yield dict(full_model)

    def _models_decomposable(self) -> t.Iterator[Model]:
        """Model enumeration for decomposable sentences."""
        if not self.satisfiable(decomposable=True):
            return
        names = tuple(self.vars())
        model_tree: t.Dict[bool, t.Any] = {}

        def leaves(
                tree: t.Dict[bool, t.Any],
                path: t.Tuple[bool, ...] = ()
        ) -> t.Iterator[t.Tuple[t.Dict[bool, t.Any], t.Tuple[bool, ...]]]:
            if not tree:
                yield tree, path
            else:
                for key, val in tree.items():
                    yield from leaves(val, path + (key,))

        for var in names:
            for leaf, path in leaves(model_tree):
                model = dict(zip(names, path))
                model[var] = True
                if self._consistent_with_model(model):
                    leaf[True] = {}
                model[var] = False
                if self._consistent_with_model(model):
                    leaf[False] = {}
                assert leaf  # at least one of them has to be satisfiable

        for leaf, path in leaves(model_tree):
            yield dict(zip(names, path))

    def _sorting_key(self) -> t.Tuple[t.Any, ...]:
        """Used for sorting nodes in a (mostly) consistent order.

        The sorting is fairly arbitrary, and mostly tuned to make .to_DOT()
        output nice. The rules are approximately:
        - Variables first
        - Variables with lower-sorting stringified names first
        - Negations last
        - Nodes with a lower height first
        - Nodes with fewer children first
        - Nodes with higher-sorting children last

        Note that Var(10) and Var("10") are sorted as equal.
        """
        raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, NNF):
            return NotImplemented
        return self._sorting_key() < other._sorting_key()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, NNF):
            return NotImplemented
        return self._sorting_key() <= other._sorting_key()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, NNF):
            return NotImplemented
        return self._sorting_key() > other._sorting_key()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, NNF):
            return NotImplemented
        return self._sorting_key() >= other._sorting_key()


class Var(NNF):
    """A variable, or its negation.

    If its name is a string, its repr will use that name directly.
    Otherwise it will use more ordinary constructor syntax.

    >>> a = Var('a')
    >>> a
    a
    >>> ~a
    ~a
    >>> b = Var('b')
    >>> a | ~b == Or({Var('a', True), Var('b', False)})
    True
    >>> Var(10)
    Var(10)
    >>> Var(('a', 'b'), False)
    ~Var(('a', 'b'))
    """

    name: Name
    true: bool

    __slots__ = ('name', 'true')

    def __init__(self, name: Name, true: bool = True) -> None:
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'true', true)

    def __eq__(self, other: t.Any) -> bool:
        return (self.__class__ is other.__class__
                and self.name == other.name
                and self.true == other.true)

    def __hash__(self) -> int:
        return hash((self.name, self.true))

    def __setattr__(self, key: str, value: object) -> None:
        raise TypeError(f"{self.__class__.__name__} objects are immutable")

    def __delattr__(self, name: str) -> None:
        raise TypeError(f"{self.__class__.__name__} objects are immutable")

    def __repr__(self) -> str:
        if isinstance(self.name, str):
            return f"{self.name}" if self.true else f"~{self.name}"
        else:
            base = f"{self.__class__.__name__}({self.name!r})"
            return base if self.true else f"~{base}"

    def __invert__(self) -> 'Var':
        return Var(self.name, not self.true)

    def _sorting_key(self) -> t.Tuple[bool, str, bool]:
        return False, str(self.name), not self.true


class Internal(NNF):
    """Base class for internal nodes, i.e. And and Or nodes."""
    children: t.FrozenSet[NNF]

    __slots__ = ()

    def __init__(self, children: t.Iterable[NNF] = ()) -> None:
        # needed because of immutability
        object.__setattr__(self, 'children', frozenset(children))

    def __eq__(self, other: t.Any) -> bool:
        return (self.__class__ is other.__class__
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash((self.children,))

    def __setattr__(self, key: str, value: object) -> None:
        raise TypeError(f"{self.__class__.__name__} objects are immutable")

    def __delattr__(self, name: str) -> None:
        raise TypeError(f"{self.__class__.__name__} objects are immutable")

    def __repr__(self) -> str:
        if self.children:
            return (f"{self.__class__.__name__}"
                    f"({{{', '.join(map(repr, self.children))}}})")
        else:
            return f"{self.__class__.__name__}()"

    def leaf(self) -> bool:
        if self.children:
            return False
        return True

    def is_simple(self) -> bool:
        """Whether all children are leaves that don't share variables."""
        variables: t.Set[Name] = set()
        for child in self.children:
            if not child.leaf():
                return False
            if isinstance(child, Var):
                if child.name in variables:
                    return False
                variables.add(child.name)
        return True

    def _sorting_key(self) -> t.Tuple[bool, int, int, str, t.List[NNF]]:
        return (True, self.height(), len(self.children),
                self.__class__.__name__, sorted(self.children, reverse=True))


class And(Internal):
    """Conjunction nodes, which are only true if all of their children are."""
    def decision_node(self) -> bool:
        if not self.children:
            return True
        return False

    def __repr__(self) -> str:
        if not self.children:
            return 'true'
        return super().__repr__()


class Or(Internal):
    """Disjunction nodes, which are true if any of their children are."""
    def decision_node(self) -> bool:
        if not self.children:
            return True  # boolean
        if len(self.children) != 2:
            return False
        child1, child2 = self.children
        if not (isinstance(child1, And) and isinstance(child2, And)):
            return False
        if not (len(child1.children) == 2 and len(child2.children) == 2):
            return False

        child11, child12 = child1.children
        child21, child22 = child2.children

        if isinstance(child11, Var):
            child1var = child11
            if not child12.decision_node():
                return False
        elif isinstance(child12, Var):
            child1var = child12
            if not child11.decision_node():
                return False
        else:
            return False

        if isinstance(child21, Var):
            child2var = child21
            if not child22.decision_node():
                return False
        elif isinstance(child22, Var):
            child2var = child22
            if not child21.decision_node():
                return False
        else:
            return False

        if child1var.name != child2var.name:
            return False

        if child1var.true == child2var.true:
            return False

        return True

    def __repr__(self) -> str:
        if not self.children:
            return 'false'
        return super().__repr__()


def decision(var: Var, if_true: NNF, if_false: NNF) -> Or:
    """Create a decision node with a variable and two branches."""
    return Or({And({var, if_true}), And({~var, if_false})})


true = And()
false = Or()


class Builder:
    """Automatically deduplicates NNF nodes as you make them.

    Usage:

    >>> builder = Builder()
    >>> var = builder.Var('A')
    >>> var2 = builder.Var('A')
    >>> var is var2
    True
    """
    # TODO: deduplicate vars that are negated using the operator
    def __init__(self, seed: t.Iterable[NNF] = ()):
        self.stored: t.Dict[NNF, NNF] = {true: true, false: false}
        for node in seed:
            self.stored[node] = node
        self.true = true
        self.false = false

    def Var(self, name: Name, true: bool = True) -> nnf.Var:
        ret = Var(name, true)
        return self.stored.setdefault(ret, ret)  # type: ignore

    def And(self, children: t.Iterable[NNF] = ()) -> nnf.And:
        ret = And(children)
        return self.stored.setdefault(ret, ret)  # type: ignore

    def Or(self, children: t.Iterable[NNF] = ()) -> nnf.Or:
        ret = Or(children)
        return self.stored.setdefault(ret, ret)  # type: ignore
