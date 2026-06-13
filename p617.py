#!/usr/bin/env python3


def integer_root(n, exponent):
    """Largest x with x**exponent <= n."""
    low, high = 1, 2
    while pow(high, exponent) <= n:
        high *= 2
    while low + 1 < high:
        mid = (low + high) // 2
        if pow(mid, exponent) <= n:
            low = mid
        else:
            high = mid
    return low


def largest_base(limit, exponent):
    base = integer_root(limit, exponent)
    while pow(base, exponent) + base > limit:
        base -= 1
    while pow(base + 1, exponent) + base + 1 <= limit:
        base += 1
    return base


def solve(limit=10**18):
    max_exponent = 0
    while (1 << (max_exponent + 1)) + 2 <= limit:
        max_exponent += 1

    total = 0
    for e in range(2, max_exponent + 1):
        chain_exponent = e
        cycle_length = 1
        while chain_exponent <= max_exponent:
            max_base = largest_base(limit, chain_exponent)
            if max_base >= 2:
                base_count = max_base - 1
                total += cycle_length * base_count

                root_exponent = e
                while root_exponent <= max_exponent and (1 << root_exponent) <= max_base:
                    total += integer_root(max_base, root_exponent) - 1
                    root_exponent *= e

            cycle_length += 1
            chain_exponent *= e

    return total


if __name__ == "__main__":
    print(solve())
