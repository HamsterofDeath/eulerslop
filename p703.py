#!/usr/bin/env python3
"""Project Euler 703: Circular logic II."""


MODULUS = 1_001_001_011


def _successor_table(bits):
    size = 1 << bits
    low_mask = size >> 1
    low_mask -= 1
    successors = [0] * size
    indegree = [0] * size

    for state in range(size):
        top = state >> (bits - 1)
        last = top & (((state >> (bits - 2)) ^ (state >> (bits - 3))) & 1)
        nxt = ((state & low_mask) << 1) | last
        successors[state] = nxt
        indegree[nxt] += 1

    return successors, indegree


def _cycle_independent_sets(unselected, selected):
    length = len(unselected)

    if length == 1:
        return unselected[0]

    first_unselected = unselected[0]
    prev0 = first_unselected
    prev1 = 0

    for i in range(1, length):
        a = unselected[i]
        b = selected[i]
        prev0, prev1 = ((prev0 + prev1) * a) % MODULUS, (prev0 * b) % MODULUS

    total = prev0 + prev1

    first_selected = selected[0]
    prev0 = 0
    prev1 = first_selected

    for i in range(1, length):
        a = unselected[i]
        b = selected[i]
        prev0, prev1 = ((prev0 + prev1) * a) % MODULUS, (prev0 * b) % MODULUS

    return (total + prev0) % MODULUS


def _count(bits):
    successors, indegree = _successor_table(bits)
    size = 1 << bits
    unselected = [1] * size
    selected = [1] * size
    queue = [node for node, degree in enumerate(indegree) if degree == 0]
    head = 0

    while head < len(queue):
        node = queue[head]
        head += 1

        parent = successors[node]
        zero = unselected[node]
        one = selected[node]
        unselected[parent] = (unselected[parent] * (zero + one)) % MODULUS
        selected[parent] = (selected[parent] * zero) % MODULUS

        indegree[parent] -= 1
        if indegree[parent] == 0:
            queue.append(parent)

    answer = 1

    for start in range(size):
        if indegree[start] == 0:
            continue

        cycle0 = []
        cycle1 = []
        node = start

        while indegree[node] != 0:
            indegree[node] = 0
            cycle0.append(unselected[node])
            cycle1.append(selected[node])
            node = successors[node]

        answer = (answer * _cycle_independent_sets(cycle0, cycle1)) % MODULUS

    return answer


def solve():
    return _count(20)


if __name__ == "__main__":
    print(solve())
