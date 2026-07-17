#!/usr/bin/env python3
"""Project Euler 871: maximum drifting subsets of cubic maps."""

from collections import deque


START = 100_001
STOP = 100_100


def maximum_drifting_subset(modulus: int) -> int:
    """Return D(f_modulus) via maximum matching on its functional graph."""
    parent = [
        (value * value % modulus * value + value + 1) % modulus
        for value in range(modulus)
    ]
    indegree = [0] * modulus
    for image in parent:
        indegree[image] += 1

    # For each rooted tree, free[v] leaves v available to its parent, while
    # best[v] may match v to one child.  Kahn peeling visits all children
    # before their parent and accumulates these two quantities.
    base = [0] * modulus
    gain = [0] * modulus
    queue = deque(
        vertex
        for vertex, degree in enumerate(indegree)
        if degree == 0
    )
    while queue:
        vertex = queue.popleft()
        free = base[vertex]
        best = free + gain[vertex]
        image = parent[vertex]
        base[image] += best
        gain[image] = max(gain[image], 1 + free - best)
        indegree[image] -= 1
        if indegree[image] == 0:
            queue.append(image)

    def path_matching(edge_weights: list[int]) -> int:
        two_back = one_back = 0
        for weight in edge_weights:
            two_back, one_back = (
                one_back,
                max(one_back, two_back + weight),
            )
        return one_back

    result = 0
    seen = [False] * modulus
    for start in range(modulus):
        if indegree[start] == 0 or seen[start]:
            continue

        cycle = []
        vertex = start
        while not seen[vertex]:
            seen[vertex] = True
            cycle.append(vertex)
            vertex = parent[vertex]

        free = [base[vertex] for vertex in cycle]
        best = [
            base[vertex] + gain[vertex]
            for vertex in cycle
        ]
        result += sum(best)
        length = len(cycle)
        if length == 1:  # A self-loop cannot belong to a matching.
            continue

        def edge_gain(first: int, second: int) -> int:
            return (
                1
                + free[first] - best[first]
                + free[second] - best[second]
            )

        if length == 2:  # The two directed arcs are one undirected edge.
            result += max(0, edge_gain(0, 1))
            continue

        edge_weights = [
            edge_gain(index, index + 1)
            for index in range(length - 1)
        ]
        without_wrap = path_matching(edge_weights)
        with_wrap = (
            edge_gain(length - 1, 0)
            + path_matching(edge_weights[1:-1])
        )
        result += max(without_wrap, with_wrap)

    return result


def solve() -> int:
    assert maximum_drifting_subset(5) == 1
    assert maximum_drifting_subset(10) == 3
    return sum(
        maximum_drifting_subset(modulus)
        for modulus in range(START, STOP + 1)
    )


if __name__ == "__main__":
    print(solve())
