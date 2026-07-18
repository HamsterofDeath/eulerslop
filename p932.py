#!/usr/bin/env python3
"""Project Euler Problem 932: 2025.

For a split with d trailing digits, put B=10**d and s=a+b.
The defining equation is equivalent to

    b(B-1) = s(B-s),

so s is an idempotent modulo B-1.  An idempotent is independently 0
or 1 modulo every prime-power factor of B-1; the Chinese remainder
theorem therefore enumerates all candidates without scanning s.
"""

from math import prod


def coprime_prime_powers(value: int) -> list[int]:
    """Return the maximal prime-power factors of value."""
    factors = []
    prime = 2
    while prime * prime <= value:
        if value % prime == 0:
            prime_power = 1
            while value % prime == 0:
                value //= prime
                prime_power *= prime
            factors.append(prime_power)
        prime += 1 if prime == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def numbers_2025(maximum_digits: int) -> set[int]:
    limit = 10**maximum_digits
    results = set()

    # Since b < a+b = sqrt(ab), no more than ceil(n/2)
    # digits can occur after the split.
    for trailing_digits in range(
        1, (maximum_digits + 1) // 2 + 1
    ):
        base = 10**trailing_digits
        modulus = base - 1
        prime_powers = coprime_prime_powers(modulus)

        for mask in range(1 << len(prime_powers)):
            zero_modulus = prod(
                prime_power
                for index, prime_power in enumerate(prime_powers)
                if mask & (1 << index)
            )
            one_modulus = modulus // zero_modulus

            if one_modulus == 1:
                root = modulus
            else:
                # root=0 (mod zero_modulus), root=1
                # (mod one_modulus).
                root = (
                    zero_modulus
                    * pow(zero_modulus, -1, one_modulus)
                    % modulus
                )

            suffix = (
                root * (base - root) // modulus
            )
            prefix = root - suffix
            if (
                prefix > 0
                and 10 ** (trailing_digits - 1)
                    <= suffix
                    < base
                and root * root < limit
            ):
                concatenation = prefix * base + suffix
                assert concatenation == root * root
                results.add(concatenation)

    return results


def total_2025(maximum_digits: int) -> int:
    return sum(numbers_2025(maximum_digits))


def solve() -> int:
    assert numbers_2025(4) == {81, 2025, 3025}
    assert total_2025(4) == 5131
    return total_2025(16)


if __name__ == "__main__":
    print(solve())
