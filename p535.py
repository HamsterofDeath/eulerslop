#!/usr/bin/env python3
from functools import lru_cache
from math import isqrt


BASE = 300_000
MOD = 1_000_000_000


def _base_sequence(limit):
    sequence = [0]
    source_index = 1
    next_new = 1

    while len(sequence) <= limit:
        value = 1 if source_index == 1 else sequence[source_index]
        for _ in range(isqrt(value)):
            sequence.append(next_new)
            next_new += 1
            if len(sequence) > limit:
                break
        if len(sequence) > limit:
            break

        sequence.append(value)
        source_index += 1

    return sequence


SEQ = _base_sequence(BASE)
T_PREFIX = [0] * (BASE + 1)
R_PREFIX = [0] * (BASE + 1)
for i in range(1, BASE + 1):
    T_PREFIX[i] = T_PREFIX[i - 1] + SEQ[i]
    R_PREFIX[i] = R_PREFIX[i - 1] + isqrt(SEQ[i])


def sqrt_floor_sum(n):
    if n <= 0:
        return 0
    root = isqrt(n)
    return (root - 1) * root * (4 * root + 1) // 6 + root * (n - root * root + 1)


@lru_cache(None)
def term(index):
    if index <= BASE:
        return SEQ[index]
    return prefix_data(index)[0] - prefix_data(index - 1)[0]


@lru_cache(None)
def prefix_data(length):
    if length <= BASE:
        return T_PREFIX[length], R_PREFIX[length]

    low = 0
    high = length
    while low < high:
        mid = (low + high + 1) // 2
        _, inserted = prefix_data(mid)
        if mid + inserted <= length:
            low = mid
        else:
            high = mid - 1

    source_terms = low
    source_sum, inserted_count = prefix_data(source_terms)

    total = source_sum + inserted_count * (inserted_count + 1) // 2
    root_sum = inserted_count + sqrt_floor_sum(inserted_count)
    remainder = length - source_terms - inserted_count

    if remainder:
        next_value = term(source_terms + 1)
        next_insert_count = isqrt(next_value)
        take = min(remainder, next_insert_count)

        total += (inserted_count + 1 + inserted_count + take) * take // 2
        root_sum += sqrt_floor_sum(inserted_count + take) - sqrt_floor_sum(inserted_count)
        remainder -= take

        if remainder:
            total += next_value
            root_sum += next_insert_count

    return total, root_sum


def T(length):
    return prefix_data(length)[0]


def solve():
    assert T(1) == 1
    assert T(20) == 86
    assert T(10**3) == 364089
    assert T(10**9) == 498676527978348241
    return T(10**18) % MOD


if __name__ == "__main__":
    print(solve())
