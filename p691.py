#!/usr/bin/env python3
"""Project Euler 691: Long substring with many repetitions."""

from array import array


LIMIT = 5_000_000


def _beatty_ratio(limit):
    """Return a Fibonacci convergent p/q for 1/phi, exact for this limit."""
    p, q = 1, 1
    while q <= limit * limit:
        p, q = q, p + q
    return p, q


def _add_state(next0, next1, link, length, occurrences, state_length, state_link, count):
    next0.append(-1)
    next1.append(-1)
    link.append(state_link)
    length.append(state_length)
    occurrences.append(count)
    return len(length) - 1


def _extend(next0, next1, link, length, occurrences, last, bit):
    current = _add_state(next0, next1, link, length, occurrences, length[last] + 1, 0, 1)
    previous = last

    if bit == 0:
        while previous != -1 and next0[previous] == -1:
            next0[previous] = current
            previous = link[previous]
        if previous == -1:
            return current

        target = next0[previous]
        if length[previous] + 1 == length[target]:
            link[current] = target
            return current

        clone = _add_state(
            next0, next1, link, length, occurrences,
            length[previous] + 1, link[target], 0,
        )
        next0[clone] = next0[target]
        next1[clone] = next1[target]
        while previous != -1 and next0[previous] == target:
            next0[previous] = clone
            previous = link[previous]
    else:
        while previous != -1 and next1[previous] == -1:
            next1[previous] = current
            previous = link[previous]
        if previous == -1:
            return current

        target = next1[previous]
        if length[previous] + 1 == length[target]:
            link[current] = target
            return current

        clone = _add_state(
            next0, next1, link, length, occurrences,
            length[previous] + 1, link[target], 0,
        )
        next0[clone] = next0[target]
        next1[clone] = next1[target]
        while previous != -1 and next1[previous] == target:
            next1[previous] = clone
            previous = link[previous]

    link[target] = clone
    link[current] = clone
    return current


def _build_automaton(size):
    next0 = array("i", [-1])
    next1 = array("i", [-1])
    link = array("i", [-1])
    length = array("I", [0])
    occurrences = array("I", [0])

    numerator, denominator = _beatty_ratio(size)
    beatty_accumulator = 0
    last = 0

    for index in range(size):
        thue_morse = index.bit_count() & 1
        beatty_accumulator += numerator
        if beatty_accumulator >= denominator:
            beatty = 1
            beatty_accumulator -= denominator
        else:
            beatty = 0

        last = _extend(next0, next1, link, length, occurrences, last, thue_morse ^ beatty)

    return link, length, occurrences


def _length_order(length, size):
    state_count = len(length)
    counts = array("I", [0]) * (size + 1)
    for state_length in length:
        counts[state_length] += 1

    total = 0
    for index, count in enumerate(counts):
        total += count
        counts[index] = total

    order = array("I", [0]) * state_count
    for state in range(state_count - 1, -1, -1):
        state_length = length[state]
        counts[state_length] -= 1
        order[counts[state_length]] = state

    return order


def _sum_repeated_lengths(size):
    link, length, occurrences = _build_automaton(size)
    order = _length_order(length, size)

    for index in range(len(order) - 1, 0, -1):
        state = order[index]
        occurrences[link[state]] += occurrences[state]

    best = array("I", [0]) * (size + 1)
    for state in range(1, len(length)):
        count = occurrences[state]
        state_length = length[state]
        if state_length > best[count]:
            best[count] = state_length

    total = 0
    maximum = 0
    for count in range(size, 0, -1):
        if best[count] > maximum:
            maximum = best[count]
        total += maximum
    return total


def solve():
    return _sum_repeated_lengths(LIMIT)


if __name__ == "__main__":
    print(solve())
