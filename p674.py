#!/usr/bin/env python3
"""Project Euler 674: Solving I-equations."""

import sys
import urllib.request


MOD = 1_000_000_000
VAR = 0
APP = 1
URL = "https://projecteuler.net/resources/documents/0674_i_expressions.txt"


class TermStore:
    def __init__(self):
        self.kind = []
        self.left = []
        self.right = []
        self.var_index = []
        self.var_names = {}
        self.var_nodes = []
        self.app_cache = {}

    def _new_node(self, kind, left=-1, right=-1, var_index=-1):
        node = len(self.kind)
        self.kind.append(kind)
        self.left.append(left)
        self.right.append(right)
        self.var_index.append(var_index)
        return node

    def variable(self, name):
        index = self.var_names.get(name)
        if index is None:
            index = len(self.var_names)
            self.var_names[name] = index
            self.var_nodes.append(self._new_node(VAR, var_index=index))
        return self.var_nodes[index]

    def app(self, left, right):
        key = (left, right)
        node = self.app_cache.get(key)
        if node is None:
            node = self._new_node(APP, left, right)
            self.app_cache[key] = node
        return node

    def parse(self, text):
        def parse_at(pos):
            if text[pos] == "I" and pos + 1 < len(text) and text[pos + 1] == "(":
                a, pos = parse_at(pos + 2)
                b, pos = parse_at(pos + 1)
                return self.app(a, b), pos + 1

            end = pos
            while end < len(text) and text[end].isalpha():
                end += 1
            return self.variable(text[pos:end]), end

        node, pos = parse_at(0)
        if pos != len(text):
            raise ValueError(f"unparsed suffix in expression: {text[pos:]}")
        return node


def read_expressions():
    with urllib.request.urlopen(URL) as f:
        return f.read().decode("utf-8").strip().splitlines()


def common_value(store, a, b):
    kind = store.kind
    left = store.left
    right = store.right
    var_index = store.var_index

    parent = {}
    binding = {}
    stack = [(a, b)]
    seen = set()

    def find(v):
        p = parent.get(v, v)
        if p != v:
            p = find(p)
            parent[v] = p
        return p

    def token(node):
        if kind[node] == VAR:
            return (VAR, find(var_index[node]))
        return (APP, node)

    def union(a_root, b_root):
        a_root = find(a_root)
        b_root = find(b_root)
        if a_root == b_root:
            return
        if b_root < a_root:
            a_root, b_root = b_root, a_root

        a_binding = binding.pop(a_root, None)
        b_binding = binding.pop(b_root, None)
        parent[b_root] = a_root

        if a_binding is not None and b_binding is not None:
            stack.append((a_binding, b_binding))
            binding[a_root] = a_binding
        elif a_binding is not None:
            binding[a_root] = a_binding
        elif b_binding is not None:
            binding[a_root] = b_binding

    while stack:
        x, y = stack.pop()
        if x == y:
            continue

        tx = token(x)
        ty = token(y)
        if tx == ty:
            continue

        key = (tx, ty) if tx < ty else (ty, tx)
        if key in seen:
            continue
        seen.add(key)

        if tx[0] == VAR and ty[0] == VAR:
            union(tx[1], ty[1])
        elif tx[0] == VAR:
            old = binding.get(tx[1])
            if old is None:
                binding[tx[1]] = ty[1]
            else:
                stack.append((old, ty[1]))
        elif ty[0] == VAR:
            old = binding.get(ty[1])
            if old is None:
                binding[ty[1]] = tx[1]
            else:
                stack.append((old, tx[1]))
        else:
            stack.append((left[tx[1]], left[ty[1]]))
            stack.append((right[tx[1]], right[ty[1]]))

    var_memo = {}
    app_memo = {}
    visiting = set()

    def evaluate(node):
        if kind[node] == VAR:
            root = find(var_index[node])
            if root in var_memo:
                return var_memo[root]

            bound = binding.get(root)
            if bound is None:
                var_memo[root] = 0
                return 0
            if root in visiting:
                raise ValueError

            visiting.add(root)
            value = evaluate(bound)
            visiting.remove(root)
            var_memo[root] = value
            return value

        if node in app_memo:
            return app_memo[node]

        x = evaluate(left[node])
        y = evaluate(right[node])
        value = ((1 + x + y) * (1 + x + y) + y - x) % MOD
        app_memo[node] = value
        return value

    try:
        return evaluate(a)
    except ValueError:
        return 0


def solve():
    sys.setrecursionlimit(100_000)
    store = TermStore()
    expressions = [store.parse(line) for line in read_expressions()]

    total = 0
    for i, expr in enumerate(expressions):
        for other in expressions[i + 1 :]:
            total = (total + common_value(store, expr, other)) % MOD
    return f"{total:09d}"


if __name__ == "__main__":
    print(solve())
