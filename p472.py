#!/usr/bin/env python3
from functools import lru_cache


MOD = 100_000_000


def segment_count(length):
    if length <= 0:
        return 0
    gap = length + 1
    if gap <= 3:
        return 1

    power = 1 << (gap.bit_length() - 1)
    return max(power // 2, gap - power)


def f(n):
    if n == 1:
        return 1

    best = -1
    count = 0
    for first in range(1, n + 1):
        left = max(0, first - 2)
        right = max(0, n - first - 1)
        seated = 1 + segment_count(left) + segment_count(right)
        if seated > best:
            best = seated
            count = 1
        elif seated == best:
            count += 1
    return count


BASE_BLOCK = [f(n) for n in range(16, 32)]
BASE_PREFIX = [0]
for n in range(1, 16):
    BASE_PREFIX.append(BASE_PREFIX[-1] + f(n))


def _middle_down_sum(q, length):
    if length <= 0:
        return 0
    total = 2 * q + 2
    rest = length - 1
    if rest:
        total += rest * q - rest * (rest - 1)
    return total


def _middle_up_sum(q, length):
    if length <= 0:
        return 0
    if length == 1:
        return 4
    rest = length - 1
    return 4 + rest * (rest + 1)


def _tail_sum(q, length):
    if length <= 0:
        return 0
    total = 3 * q + 3
    rest = length - 1
    if rest:
        total += rest * (q + 3) - rest * (rest + 1) // 2
    return total


@lru_cache(None)
def _block_prefix(q, length):
    if length <= 0:
        return 0
    if q == 4:
        return sum(BASE_BLOCK[:length])

    length = min(length, 4 * q)
    first_cut = 3 * q // 2 + 1
    second_cut = 2 * q
    third_cut = 3 * q + 1

    if length <= first_cut:
        return _block_prefix(q // 2, length)

    total = _block_prefix(q // 2, first_cut)
    if length <= second_cut:
        return total + _middle_down_sum(q, length - first_cut)

    total += _middle_down_sum(q, second_cut - first_cut)
    if length <= third_cut:
        return total + _middle_up_sum(q, length - second_cut)

    total += _middle_up_sum(q, third_cut - second_cut)
    return total + _tail_sum(q, length - third_cut)


@lru_cache(None)
def summatory(limit):
    if limit <= 0:
        return 0
    if limit < 16:
        return BASE_PREFIX[limit]

    power = 1 << (limit.bit_length() - 1)
    q = power // 4
    return summatory(4 * q - 1) + _block_prefix(q, limit - 4 * q + 1)


def solve():
    assert f(1) == 1
    assert f(15) == 9
    assert f(20) == 6
    assert f(500) == 16
    assert summatory(20) == 83
    assert summatory(500) == 13343
    return summatory(10**12) % MOD


if __name__ == "__main__":
    print(solve())
