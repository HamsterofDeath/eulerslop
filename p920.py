"""Project Euler Problem 920: Tau Numbers.

For fixed k, write x = product(p^e). The conditions are

    product(e+1) = k

and, because k divides x, every prime p dividing k must receive an exponent
at least v_p(k). We enumerate unordered multiplicative partitions of k, which
are the possible exponent multisets. Only 17,562 partitions have even their
unconstrained minimum below 10^16.

For each multiset, all required primes must be used; the remaining bases are
the smallest available primes. A small branch-and-bound assignment then finds
the least product satisfying the required exponent lower bounds.
"""

from math import isqrt


LIMIT = 10**16
MAXIMUM_DIVISOR_COUNT = 41_472


def primes_through(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [number for number in range(2, limit + 1) if sieve[number]]


PRIMES = primes_through(MAXIMUM_DIVISOR_COUNT)
SMALL_PRIMES = PRIMES[:20]


def factorization(number: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    for prime in PRIMES:
        if prime * prime > number:
            break
        while number % prime == 0:
            factors[prime] = factors.get(prime, 0) + 1
            number //= prime
    if number > 1:
        factors[number] = 1
    return factors


def constrained_minimum(exponents: tuple[int, ...], divisor_count: int) -> int:
    """Find the least x for one exponent multiset and tau(x)."""
    required = factorization(divisor_count)
    base_count = len(exponents)
    if len(required) > base_count:
        return LIMIT + 1

    optional_count = base_count - len(required)
    optional_primes = [
        prime for prime in SMALL_PRIMES if prime not in required
    ][:optional_count]
    bases = sorted([*required, *optional_primes])

    # Rearrangement gives a lower bound before considering required exponents.
    unconstrained = 1
    for prime, exponent in zip(bases, exponents):
        unconstrained *= prime**exponent
    if unconstrained > LIMIT:
        return LIMIT + 1

    if all(
        exponent >= required.get(prime, 0)
        for prime, exponent in zip(bases, exponents)
    ):
        return unconstrained

    best = LIMIT + 1

    def assign(
        base_index: int,
        remaining: tuple[int, ...],
        product: int,
    ) -> None:
        nonlocal best

        # Assigning remaining exponents in descending order is an optimistic
        # rearrangement bound, even if it violates a required lower bound.
        lower_bound = product
        for prime, exponent in zip(bases[base_index:], remaining):
            lower_bound *= prime**exponent
            if lower_bound >= best:
                return

        if base_index == base_count:
            best = product
            return

        prime = bases[base_index]
        minimum_exponent = required.get(prime, 0)
        previous_exponent = None

        for index, exponent in enumerate(remaining):
            if exponent == previous_exponent:
                continue
            previous_exponent = exponent
            if exponent < minimum_exponent:
                continue

            next_product = product * prime**exponent
            if next_product >= best:
                continue
            assign(
                base_index + 1,
                remaining[:index] + remaining[index + 1 :],
                next_product,
            )

    assign(0, exponents, 1)
    return best


def minimal_tau_numbers() -> dict[int, int]:
    minima = {1: 1}

    def enumerate_partitions(
        divisor_count: int,
        maximum_factor: int,
        exponents: tuple[int, ...],
        standard_minimum: int,
    ) -> None:
        if exponents:
            candidate = constrained_minimum(exponents, divisor_count)
            if candidate <= LIMIT:
                minima[divisor_count] = min(
                    minima.get(divisor_count, LIMIT + 1),
                    candidate,
                )

        next_prime = SMALL_PRIMES[len(exponents)]
        largest_factor = min(
            maximum_factor,
            MAXIMUM_DIVISOR_COUNT // divisor_count,
        )

        # Factors (e+1) are nonincreasing, so every exponent multiset appears
        # exactly once and its standard prime assignment is minimal.
        for factor in range(2, largest_factor + 1):
            next_minimum = standard_minimum * next_prime ** (factor - 1)
            if next_minimum > LIMIT:
                break
            enumerate_partitions(
                divisor_count * factor,
                factor,
                exponents + (factor - 1,),
                next_minimum,
            )

    enumerate_partitions(1, MAXIMUM_DIVISOR_COUNT, (), 1)
    return minima


def solve() -> int:
    minima = minimal_tau_numbers()
    assert minima[8] == 24
    assert minima[12] == 60
    assert minima[16] == 384
    assert sum(value for value in minima.values() if value <= 1_000) == 3_189
    return sum(minima.values())


if __name__ == "__main__":
    print(solve())
