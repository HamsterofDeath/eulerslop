#!/usr/bin/env python3
"""Project Euler 698: 123 Numbers."""

from functools import cache
from math import factorial


TARGET_INDEX = 111_111_111_111_222_333
MODULUS = 123_123_123


@cache
def _is_123_number(n):
    if n == 1:
        return True

    digits = str(n)
    if any(digit not in "123" for digit in digits):
        return False

    return all(
        count == 0 or _is_123_number(count)
        for count in (digits.count("1"), digits.count("2"), digits.count("3"))
    )


@cache
def _valid_counts_up_to(limit):
    return tuple(n for n in range(1, limit + 1) if _is_123_number(n))


@cache
def _factorials(limit):
    return tuple(factorial(n) for n in range(limit + 1))


@cache
def _count_triples_for_length(length):
    valid = set(_valid_counts_up_to(length))
    options = (0,) + tuple(sorted(valid))
    facts = _factorials(length)
    triples = []
    total = 0

    for ones in options:
        for twos in options:
            threes = length - ones - twos
            if threes < 0:
                continue
            if threes == 0 or threes in valid:
                triples.append((ones, twos, threes))
                total += facts[length] // facts[ones] // facts[twos] // facts[threes]

    return tuple(triples), total


def _completion_count(length, triples, used):
    remaining = length - sum(used)
    facts = _factorials(length)
    total = 0

    for counts in triples:
        if all(counts[i] >= used[i] for i in range(3)):
            ways = facts[remaining]
            for i in range(3):
                ways //= facts[counts[i] - used[i]]
            total += ways

    return total


def _target_length_and_offset(index):
    before = 0
    length = 0

    while before < index:
        length += 1
        triples, count = _count_triples_for_length(length)
        if before + count >= index:
            return length, triples, index - before
        before += count

    raise RuntimeError("unreachable")


def _unrank_123_number_mod(index, modulus):
    length, triples, offset = _target_length_and_offset(index)
    used = [0, 0, 0]
    value = 0

    for _ in range(length):
        for digit_index, digit in enumerate((1, 2, 3)):
            used[digit_index] += 1
            count = _completion_count(length, triples, used)
            if offset > count:
                offset -= count
                used[digit_index] -= 1
                continue

            value = (value * 10 + digit) % modulus
            break

    return value


def solve():
    return _unrank_123_number_mod(TARGET_INDEX, MODULUS)


if __name__ == "__main__":
    print(solve())
