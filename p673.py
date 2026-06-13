#!/usr/bin/env python3
"""Project Euler 673: Beds and Desks."""

from collections import defaultdict
import urllib.request


MOD = 999_999_937
N = 500
BASE_URL = "https://projecteuler.net/resources/documents"


def read_pairs(name):
    url = f"{BASE_URL}/{name}"
    with urllib.request.urlopen(url) as f:
        lines = f.read().decode("utf-8").strip().splitlines()
    return [tuple(map(int, line.split(","))) for line in lines if line]


def count_automorphisms(n, beds, desks):
    adj = [[] for _ in range(n)]
    for color, pairs in ((0, beds), (1, desks)):
        for a, b in pairs:
            a -= 1
            b -= 1
            adj[a].append((b, color))
            adj[b].append((a, color))

    def path_colors(start):
        colors = []
        prev = -1
        cur = start
        while True:
            nxt = [(v, c) for v, c in adj[cur] if v != prev]
            if not nxt:
                return tuple(colors)
            v, color = nxt[0]
            colors.append(color)
            prev, cur = cur, v

    seen = [False] * n
    components = defaultdict(lambda: [0, 0])

    for start in range(n):
        if seen[start]:
            continue

        stack = [start]
        seen[start] = True
        vertices = []
        degree_sum = 0
        while stack:
            v = stack.pop()
            vertices.append(v)
            degree_sum += len(adj[v])
            for w, _ in adj[v]:
                if not seen[w]:
                    seen[w] = True
                    stack.append(w)

        size = len(vertices)
        edges = degree_sum // 2
        if size == 1:
            signature = ("single",)
            automorphisms = 1
        elif edges == size:
            signature = ("cycle", size)
            automorphisms = size
        else:
            ends = [v for v in vertices if len(adj[v]) == 1]
            forward = path_colors(ends[0])
            backward = path_colors(ends[1])
            signature = ("path", min(forward, backward))
            automorphisms = 2 if forward == backward else 1

        components[signature][0] += 1
        components[signature][1] = automorphisms

    total = 1
    for multiplicity, automorphisms in components.values():
        total = total * pow(automorphisms, multiplicity, MOD) % MOD
        for k in range(2, multiplicity + 1):
            total = total * k % MOD
    return total


def solve():
    beds = read_pairs("0673_beds.txt")
    desks = read_pairs("0673_desks.txt")
    return count_automorphisms(N, beds, desks)


if __name__ == "__main__":
    print(solve())
