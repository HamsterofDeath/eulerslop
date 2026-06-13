#!/usr/bin/env python3
"""Project Euler 663: sums of maximal subarrays after Tribonacci updates."""

from array import array


N = 10_000_003
FIRST = 10_000_000
LAST = 10_200_000


def _advance(a: int, b: int, c: int, mod: int) -> tuple[int, int, int]:
    d = a + b + c
    if d >= mod:
        d -= mod
        if d >= mod:
            d -= mod

    e = b + c + d
    if e >= mod:
        e -= mod
        if e >= mod:
            e -= mod

    return c, d, e


def _add_initial_updates(total: array, size: int, count: int, mod: int) -> tuple[int, int, int]:
    a, b, c = 0, 0, 1
    offset = size
    shift = 1 - mod

    for _ in range(count):
        total[offset + a] += b + b + shift
        a, b, c = _advance(a, b, c, mod)

    return a, b, c


def _build_tree(total: array, pref: array, suff: array, best: array, size: int, n: int) -> None:
    end = size + n
    for i in range(size, end):
        value = total[i]
        if value > 0:
            pref[i] = value
            suff[i] = value
            best[i] = value

    for i in range(size - 1, 0, -1):
        left = i + i
        right = left + 1

        left_sum = total[left]
        right_sum = total[right]
        left_pref = pref[left]
        right_pref = pref[right]
        left_suff = suff[left]
        right_suff = suff[right]
        left_best = best[left]
        right_best = best[right]

        total_sum = left_sum + right_sum
        prefix = left_pref
        candidate = left_sum + right_pref
        if candidate > prefix:
            prefix = candidate

        suffix = right_suff
        candidate = right_sum + left_suff
        if candidate > suffix:
            suffix = candidate

        maximum = left_best if left_best > right_best else right_best
        candidate = left_suff + right_pref
        if candidate > maximum:
            maximum = candidate

        total[i] = total_sum
        pref[i] = prefix
        suff[i] = suffix
        best[i] = maximum


def _apply_update(
    total: array,
    pref: array,
    suff: array,
    best: array,
    size: int,
    pos: int,
    delta: int,
) -> int:
    i = size + pos
    value = total[i] + delta
    total[i] = value
    clipped = value if value > 0 else 0
    pref[i] = clipped
    suff[i] = clipped
    best[i] = clipped

    i >>= 1
    while i:
        left = i + i
        right = left + 1

        left_sum = total[left]
        right_sum = total[right]
        left_pref = pref[left]
        right_pref = pref[right]
        left_suff = suff[left]
        right_suff = suff[right]
        left_best = best[left]
        right_best = best[right]

        total_sum = left_sum + right_sum
        prefix = left_pref
        candidate = left_sum + right_pref
        if candidate > prefix:
            prefix = candidate

        suffix = right_suff
        candidate = right_sum + left_suff
        if candidate > suffix:
            suffix = candidate

        maximum = left_best if left_best > right_best else right_best
        candidate = left_suff + right_pref
        if candidate > maximum:
            maximum = candidate

        total[i] = total_sum
        pref[i] = prefix
        suff[i] = suffix
        best[i] = maximum
        i >>= 1

    return best[1]


def tribonacci_max_sum_delta(n: int, first: int, last: int) -> int:
    size = 1 << (n - 1).bit_length()
    tree_len = size + size

    total = array("q", [0]) * tree_len
    a, b, c = _add_initial_updates(total, size, first, n)

    pref = array("q", [0]) * tree_len
    suff = array("q", [0]) * tree_len
    best = array("q", [0]) * tree_len
    _build_tree(total, pref, suff, best, size, n)

    answer = 0
    shift = 1 - n
    for _ in range(last - first):
        answer += _apply_update(total, pref, suff, best, size, a, b + b + shift)
        a, b, c = _advance(a, b, c, n)
    return answer


def solve() -> int:
    return tribonacci_max_sum_delta(N, FIRST, LAST)


if __name__ == "__main__":
    print(solve())
