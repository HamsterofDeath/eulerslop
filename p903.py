#!/usr/bin/env python3
"""Project Euler 903: ranks of every permutation power."""

MODULUS = 1_000_000_007


def rank_power_sum(n: int) -> int:
    """Return Q(n) modulo 1,000,000,007.

    The distribution of pi^i is invariant under conjugation.  Averaging
    the Lehmer-code comparison at positions a<b over a conjugacy class
    shows that its rank depends only on f, the number of fixed points,
    and c, the number of 2-cycles:

      Pr(q(b)<q(a)) =
        1/2 + (2c-f(f-1))/(2n(n-1))
        + (b-a-1)(f^2-(n+1)f+n-2c)/(n(n-1)(n-2)).

    It remains to sum f, f^2, and c over every pi and every exponent.
    A cycle has one fixed-point-producing exponent residue; an even
    cycle has one residue that produces 2-cycles.  For f^2, two cycles
    of lengths a,b are simultaneously fixed with frequency
    1/lcm(a,b), producing a gcd(a,b) term.
    """
    if n == 1:
        return 1

    inverse_two = (MODULUS + 1) // 2

    inverses = [0] * (n + 1)
    inverses[1] = 1
    harmonic = [0] * (n + 1)
    square_harmonic = [0] * (n + 1)

    factorial_n = 1
    distance_weight = 0
    for value in range(1, n + 1):
        if value > 1:
            inverses[value] = (
                MODULUS
                - MODULUS // value * inverses[MODULUS % value]
                % MODULUS
            )

        harmonic[value] = (
            harmonic[value - 1] + inverses[value]
        ) % MODULUS
        square_harmonic[value] = (
            square_harmonic[value - 1]
            + inverses[value] * inverses[value]
        ) % MODULUS

        factorial_n = factorial_n * value % MODULUS
        if value < n:
            distance_weight += (
                factorial_n
                * value
                % MODULUS
                * (value - 1)
                % MODULUS
                * inverse_two
            )
            distance_weight %= MODULUS

    # gcd(a,b) = sum_{d|a,b} phi(d).  After a=dx, b=dy,
    #
    # sum_{x+y<=N} 1/(xy) = H_N^2-H_N^(2).
    half = n // 2
    totients = list(range(half + 1))
    for prime in range(2, half + 1):
        if totients[prime] == prime:
            for multiple in range(prime, half + 1, prime):
                totients[multiple] -= (
                    totients[multiple] // prime
                )

    gcd_pair_sum = 0
    for divisor in range(1, half + 1):
        quotient = n // divisor
        inner_sum = (
            harmonic[quotient] * harmonic[quotient]
            - square_harmonic[quotient]
        ) % MODULUS
        gcd_pair_sum += (
            totients[divisor]
            * inverses[divisor]
            % MODULUS
            * inverses[divisor]
            % MODULUS
            * inner_sum
        )
        gcd_pair_sum %= MODULUS

    sample_count = factorial_n * factorial_n % MODULUS

    sum_fixed = sample_count * harmonic[n] % MODULUS
    sum_two_cycles = (
        sample_count
        * harmonic[half]
        % MODULUS
        * inverse_two
        % MODULUS
        * inverse_two
    ) % MODULUS
    sum_fixed_squared = (
        sample_count * (n + gcd_pair_sum)
    ) % MODULUS

    first_correction = (
        2 * sum_two_cycles
        - sum_fixed_squared
        + sum_fixed
    ) % MODULUS
    second_correction = (
        sum_fixed_squared
        - (n + 1) * sum_fixed
        + n * sample_count
        - 2 * sum_two_cycles
    ) % MODULUS

    pair_denominator = n * (n - 1) % MODULUS
    inverse_pair_denominator = pow(
        pair_denominator,
        MODULUS - 2,
        MODULUS,
    )

    # For r=n-a:
    # sum_a (n-a)(n-a)! = n!-1.
    position_weight = (factorial_n - 1) % MODULUS
    answer = (
        sample_count
        * (1 + position_weight * inverse_two)
    ) % MODULUS
    answer += (
        position_weight
        * inverse_two
        % MODULUS
        * first_correction
        % MODULUS
        * inverse_pair_denominator
    )

    if n > 2:
        answer += (
            distance_weight
            * second_correction
            % MODULUS
            * inverse_pair_denominator
            % MODULUS
            * pow(n - 2, MODULUS - 2, MODULUS)
        )

    return answer % MODULUS


def solve() -> int:
    assert rank_power_sum(2) == 5
    assert rank_power_sum(3) == 88
    assert rank_power_sum(6) == 133_103_808
    assert rank_power_sum(10) == 468_421_536
    return rank_power_sum(10**6)


if __name__ == "__main__":
    print(solve())
