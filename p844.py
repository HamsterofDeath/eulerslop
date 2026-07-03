#!/usr/bin/env python3
"""Project Euler 844: k-Markov numbers from bounded mutation trees."""

from bisect import insort


LIMIT = 10**18
MOD = 1_405_695_061


def three_branch_value(k: int) -> int:
    first = k - 1
    second = k * first - 1
    return k * first * second - 1


def full_markov_sum(k: int, limit: int, modulus: int | None = None) -> int:
    """Enumerate all distinct k-Markov numbers <= limit for one small k."""
    seen_states = {()}
    stack = [()]
    values = {1}
    if k - 1 <= limit:
        values.add(k - 1)

    while stack:
        state = stack.pop()
        product = 1
        for value in state:
            product *= value

        if len(state) < k:
            new_value = k * product - 1
            if 1 < new_value <= limit:
                new_state = tuple(sorted(state + (new_value,)))
                if new_state not in seen_states:
                    seen_states.add(new_state)
                    stack.append(new_state)
                values.add(new_value)

        for index, old_value in enumerate(state):
            new_value = k * (product // old_value) - old_value
            new_state_list = list(state)
            new_state_list.pop(index)
            if new_value > 1:
                if new_value > limit:
                    continue
                insort(new_state_list, new_value)
                values.add(new_value)
            new_state = tuple(new_state_list)
            if new_state not in seen_states:
                seen_states.add(new_state)
                stack.append(new_state)

    total = sum(values)
    return total if modulus is None else total % modulus


def full_s(limit_k: int, limit_n: int) -> int:
    return sum(full_markov_sum(k, limit_n) for k in range(3, limit_k + 1))


def max_k_with(limit: int, fn) -> int:
    lo, hi = 3, 3
    while fn(hi) <= limit:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if fn(mid) <= limit:
            lo = mid
        else:
            hi = mid - 1
    return lo


def sum_linear(a: int, b: int) -> int:
    if b < a:
        return 0
    return (a + b) * (b - a + 1) // 2


def sum_squares(a: int, b: int) -> int:
    if b < a:
        return 0

    def prefix(n: int) -> int:
        return n * (n + 1) * (2 * n + 1) // 6

    return prefix(b) - prefix(a - 1)


def sum_cubes(a: int, b: int) -> int:
    if b < a:
        return 0

    def prefix(n: int) -> int:
        return (n * (n + 1) // 2) ** 2

    return prefix(b) - prefix(a - 1)


def target_sum() -> int:
    # For k above this cutoff, any branch with three non-one entries already
    # exceeds LIMIT, so only the two-non-one chain can add values beyond 1,k-1.
    cutoff = max_k_with(LIMIT, three_branch_value)

    total = 0
    for k in range(3, cutoff + 1):
        total = (total + full_markov_sum(k, LIMIT, MOD)) % MOD

    start = cutoff + 1
    total += sum_linear(start, LIMIT)  # 1 + (k - 1) for each remaining k.

    u2_limit = max_k_with(LIMIT, lambda k: k * k - k - 1)
    total += sum_squares(start, u2_limit) - sum_linear(start, u2_limit)
    total -= max(0, u2_limit - start + 1)

    u3_limit = max_k_with(LIMIT, lambda k: k**3 - k * k - 2 * k + 1)
    total += sum_cubes(start, u3_limit) - sum_squares(start, u3_limit)
    total -= 2 * sum_linear(start, u3_limit)
    total += max(0, u3_limit - start + 1)

    return total % MOD


def solve() -> int:
    assert full_s(4, 100) == 229
    assert full_s(10, 10**8) == 2_383_369_980
    return target_sum()


if __name__ == "__main__":
    print(solve())
