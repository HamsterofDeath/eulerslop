#!/usr/bin/env python3
"""Project Euler 813: sparse Frobenius powers for XOR multiplication."""


MOD = 1_000_000_007


def xor_power_value(exponent: int) -> int:
    exponents = {0}
    bit = 0
    n = exponent
    while n:
        if n & 1:
            shift = 1 << bit
            updated: set[int] = set()
            for current in exponents:
                for add in (0, shift, 3 * shift):
                    value = current + add
                    if value in updated:
                        updated.remove(value)
                    else:
                        updated.add(value)
            exponents = updated
        n >>= 1
        bit += 1
    return sum(pow(2, e, MOD) for e in exponents) % MOD


def solve() -> int:
    assert xor_power_value(2) == 69
    return xor_power_value(8**12 * 12**8)


if __name__ == "__main__":
    print(solve())
