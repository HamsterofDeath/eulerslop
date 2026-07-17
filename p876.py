#!/usr/bin/env python3
"""Project Euler 876: reflections of an ideal rational triangle."""


def reflection_distance(numerator: int, denominator: int) -> int:
    """Return the minimum reflections taking z to 0, -1, or infinity.

    Put x = -z.  The three operations on (a, b, c) act on x as

        x -> -x,  x -> 2-x,  x -> x/(2x-1).

    These are the side reflections of the ideal triangle with vertices
    0, 1, and infinity.  A rational outside those vertices has exactly
    one reflection that moves it towards the triangle.

    Alternating two reflections walks around one vertex.  Such a walk is
    a translation by 2 in x, 1/x, or 1/(x-1), so the six tests below
    batch an entire run at once instead of using a subtractive algorithm.
    """
    p, q = -numerator, denominator
    if q < 0:
        p, q = -p, -q

    distance = 0
    while p != 0 and q != 0 and p != q:
        # Alternating around infinity: x changes by 2.
        if p > 2 * q:
            steps = (p - 1) // (2 * q)
            p -= 2 * steps * q
            distance += 2 * steps
            continue
        if p < -q:
            steps = (-p + q - 1) // (2 * q)
            p += 2 * steps * q
            distance += 2 * steps
            continue

        # Alternating around zero: 1/x changes by 2.
        if -q < p < 0:
            magnitude = -p
            steps = (q + magnitude - 1) // (2 * magnitude)
            q += 2 * steps * p
            distance += 2 * steps
            if q < 0:
                p, q = -p, -q
            continue
        if 0 < p and 2 * p < q:
            steps = (q - 1) // (2 * p)
            q -= 2 * steps * p
            distance += 2 * steps
            continue

        # Alternating around one: 1/(x-1) changes by 2.
        if 2 * p > q and p < q:
            offset = p - q
            steps = (q - 1) // (-2 * offset)
            q += 2 * steps * offset
            p = q + offset
            distance += 2 * steps
            if q < 0:
                p, q = -p, -q
            continue
        if p > q and 2 * (p - q) < q:
            offset = p - q
            steps = (q - 1) // (2 * offset)
            q -= 2 * steps * offset
            p = q + offset
            distance += 2 * steps
            if q < 0:
                p, q = -p, -q
            continue

        # A boundary case needs one ordinary side reflection.
        if p > q:
            p = 2 * q - p
        elif p < 0:
            p = -p
        else:
            p, q = p, 2 * p - q
            if q < 0:
                p, q = -p, -q
        distance += 1

    return distance


def smooth_divisors(number: int) -> list[int]:
    """Return all divisors of a number whose prime factors are 2, 3, and 5."""
    divisors = [1]
    remaining = number
    for prime in (2, 3, 5):
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1

        old_divisors = divisors
        divisors = []
        power = 1
        for _ in range(exponent + 1):
            divisors.extend(divisor * power for divisor in old_divisors)
            power *= prime

    assert remaining == 1
    return divisors


def summatory_steps(a: int, b: int) -> int:
    """Compute F(a, b) by enumerating all triples that can reach zero."""
    product = 4 * a * b
    total = 0

    # The invariant
    #
    #   Q = a^2+b^2+c^2-2ab-2ac-2bc
    #
    # must be a square d^2 if a coordinate can become zero.  With
    # x = c-a-b this is equivalent to
    #
    #   (x-d)(x+d) = 4ab.
    #
    # Conversely, for every such factor pair the two rational isotropic
    # directions are (x-d)/(2a) and (x+d)/(2a).  Reaching a zero
    # coordinate is precisely taking either direction to 0, -1, or
    # infinity, which reflection_distance computes.
    for factor in smooth_divisors(product):
        other = product // factor
        if factor > other or (factor - other) % 2 != 0:
            continue

        total += min(
            reflection_distance(factor, 2 * a),
            reflection_distance(other, 2 * a),
        )

        # The negative factor pair gives x < 0 and hence a second c.
        # It is admissible only while c = a+b+x remains positive.
        if factor + other < 2 * (a + b):
            total += min(
                reflection_distance(-factor, 2 * a),
                reflection_distance(-other, 2 * a),
            )

    return total


def solve() -> int:
    assert summatory_steps(6, 10) == 17
    assert summatory_steps(36, 100) == 179
    return sum(summatory_steps(6**k, 10**k) for k in range(1, 19))


if __name__ == "__main__":
    print(solve())
