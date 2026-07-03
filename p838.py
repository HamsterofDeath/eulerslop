#!/usr/bin/env python3
"""Project Euler 838: weighted bipartite vertex cover after forced factors."""

from collections import deque
from math import isqrt, log


class Dinic:
    def __init__(self, n: int):
        self.graph: list[list[list[float | int]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, capacity: float) -> None:
        self.graph[u].append([v, capacity, len(self.graph[v])])
        self.graph[v].append([u, 0.0, len(self.graph[u]) - 1])

    def max_flow(self, source: int, sink: int) -> float:
        result = 0.0
        while True:
            level = [-1] * len(self.graph)
            level[source] = 0
            queue = deque([source])
            while queue:
                u = queue.popleft()
                for v, capacity, _ in self.graph[u]:
                    if capacity > 1e-12 and level[v] < 0:
                        level[v] = level[u] + 1
                        queue.append(v)
            if level[sink] < 0:
                return result

            it = [0] * len(self.graph)

            def dfs(u: int, flow: float) -> float:
                if u == sink:
                    return flow
                while it[u] < len(self.graph[u]):
                    edge = self.graph[u][it[u]]
                    v, capacity, reverse = edge
                    if capacity > 1e-12 and level[v] == level[u] + 1:
                        pushed = dfs(v, min(flow, capacity))
                        if pushed > 1e-12:
                            edge[1] -= pushed
                            self.graph[v][reverse][1] += pushed
                            return pushed
                    it[u] += 1
                return 0.0

            while True:
                pushed = dfs(source, 1e100)
                if pushed <= 1e-12:
                    break
                result += pushed


def smallest_prime_factors(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    for i in range(2, isqrt(limit) + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def prime_factors(n: int, spf: list[int]) -> set[int]:
    result = set()
    while n > 1:
        p = spf[n]
        result.add(p)
        while n % p == 0:
            n //= p
    return result


def log_f(limit: int) -> float:
    spf = smallest_prime_factors(limit)
    primes = [n for n in range(2, limit + 1) if spf[n] == n]
    selected = {p for p in primes if p % 10 == 3}

    items = [prime_factors(n, spf) for n in range(3, limit + 1, 10)]
    changed = True
    while changed:
        changed = False
        remaining = []
        for factors in items:
            if factors & selected:
                continue
            factors = factors - selected
            if len(factors) == 1:
                selected |= factors
                changed = True
            else:
                remaining.append(factors)
        items = remaining

    edges: set[tuple[int, int]] = set()
    left: set[int] = set()
    right: set[int] = set()
    for factors in items:
        sevens = [p for p in factors if p % 10 == 7]
        nines = [p for p in factors if p % 10 == 9]
        for a in sevens:
            for b in nines:
                if a * b <= limit:
                    edges.add((a, b))
                    left.add(a)
                    right.add(b)
                    break
            else:
                continue
            break

    left = set(sorted(left))
    right = set(sorted(right))
    left_index = {p: i for i, p in enumerate(sorted(left))}
    right_index = {p: i + len(left_index) for i, p in enumerate(sorted(right))}
    source = len(left_index) + len(right_index)
    sink = source + 1
    flow = Dinic(sink + 1)
    for p, i in left_index.items():
        flow.add_edge(source, i, log(p))
    for a, b in edges:
        flow.add_edge(left_index[a], right_index[b], 1e50)
    for p, i in right_index.items():
        flow.add_edge(i, sink, log(p))

    return sum(log(p) for p in selected) + flow.max_flow(source, sink)


def solve() -> str:
    assert f"{log_f(40):.6f}" == "6.799056"
    assert f"{log_f(2800):.6f}" == "715.019337"
    return f"{log_f(1_000_000):.6f}"


if __name__ == "__main__":
    print(solve())
