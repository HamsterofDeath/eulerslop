#!/usr/bin/env python3
from math import factorial


def count_ways(num_dice, sides, top, target):
    """Count ordered rolls of num_dice dice (1..sides) whose top `top` sum to target."""
    rest = num_dice - top
    fact = [factorial(i) for i in range(num_dice + 1)]
    total = 0

    # Enumerate non-increasing `top`-tuples of values in 1..sides summing to target.
    def gen(remaining_slots, remaining_sum, max_val, counts):
        nonlocal total
        if remaining_slots == 0:
            if remaining_sum != 0:
                return
            # counts: dict value -> multiplicity within the top tuple
            m = min(counts)          # value of the lowest die in the top group
            t = counts[m]            # how many of the top tuple equal m
            denom_high = 1
            for v, c in counts.items():
                if v != m:
                    denom_high *= fact[c]
            # The other `rest` dice must be <= m; e of them equal m (joining the
            # tie group), the remaining rest - e are each anything in 1..m-1.
            for e in range(rest + 1):
                total += (fact[num_dice]
                          // (denom_high * fact[t + e] * fact[rest - e])
                          * (m - 1) ** (rest - e))
            return
        # Prune: remaining slots must be able to reach remaining_sum.
        if remaining_sum < remaining_slots or remaining_sum > remaining_slots * max_val:
            return
        for v in range(min(max_val, remaining_sum), 0, -1):
            counts[v] = counts.get(v, 0) + 1
            gen(remaining_slots - 1, remaining_sum - v, v, counts)
            counts[v] -= 1
            if counts[v] == 0:
                del counts[v]

    gen(top, target, sides, {})
    return total


def solve():
    assert count_ways(5, 6, 3, 15) == 1111
    return count_ways(20, 12, 10, 70)


if __name__ == "__main__":
    print(solve())
