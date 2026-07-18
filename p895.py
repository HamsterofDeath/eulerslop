#!/usr/bin/env python3
"""Project Euler Problem 895: Gold & Silver Coin Game II.

A stack is a red-blue Hackenbush stalk, with gold worth +1 and silver
worth -1.  Its game value is therefore a dyadic rational.  A fair
three-stack position has values summing to zero, while balance says
their gold-minus-silver counts also sum to zero.

Mixed stacks have value

    k + (2*x + 1) / 2**t

and coin difference

    k + offset + 2*popcount(x) - (t - 1).

Splitting triples by the number of mixed stacks leaves cases with zero,
two, or three mixed stacks.  In the last case, the denominators must be
(T, T, u), u < T.  A carry DP counts compatible numerators, while
geometrically weighted quadratic prefix sums eliminate the T loop.
"""


TARGET = 9_898
MODULUS = 989_898_989


def ceil_div(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def unbounded_triple_count(total: int) -> int:
    """Count nonnegative triples with the given sum."""
    if total < 0:
        return 0
    return (total + 2) * (total + 1) // 2


def bounded_triple_count(lengths: list[int], total: int) -> int:
    """Count x_i in [0, lengths[i]) whose sum is total."""
    answer = 0
    for mask in range(8):
        shifted = total
        parity = 0
        for index, length in enumerate(lengths):
            if mask & (1 << index):
                shifted -= length
                parity ^= 1
        term = unbounded_triple_count(shifted)
        answer += -term if parity else term
    return answer


def count_exact(m: int) -> int:
    """Straightforward form of the formulas, for sample checks."""
    all_monochrome = 3 * m * (m - 1)

    two_mixed = 0
    for exponent in range(1, m):
        initial_run_choices = m - exponent
        two_mixed += (
            (1 << (exponent - 1))
            * initial_run_choices
            * (initial_run_choices - 1)
        )
    two_mixed *= 6

    three_mixed = 0
    # For u bits, carry0[c]/carry1[c] count numerator triples
    # ending with that carry and having c internal carry-one states.
    carry0 = [1]
    carry1 = [1]

    for u in range(1, m - 1):
        for largest_exponent in range(u + 1, m):
            free_low_bits = largest_exponent - u - 1
            low_bit_choices = 1 << free_low_bits

            for fractional_sum in (1, 2):
                final_carry = fractional_sum - 1
                for short_position in range(3):
                    exponents = [
                        largest_exponent,
                        largest_exponent,
                        largest_exponent,
                    ]
                    exponents[short_position] = u

                    # A set bit marks a silver-starting stack.
                    for signs in range(8):
                        negative_count = signs.bit_count()
                        numerator = (
                            fractional_sum
                            - negative_count
                            + u
                            + 1
                            - 4 * final_carry
                        )
                        if numerator % 2:
                            continue
                        carry_ones = numerator // 2
                        if not 0 <= carry_ones < u:
                            continue
                        high_bit_choices = (
                            carry0[carry_ones]
                            if final_carry == 0
                            else carry1[carry_ones]
                        )

                        lower_bounds = []
                        lengths = []
                        for position, exponent in enumerate(exponents):
                            run_choices = m - exponent
                            if signs & (1 << position):
                                lower_bounds.append(-run_choices)
                            else:
                                lower_bounds.append(0)
                            lengths.append(run_choices)

                        base_total = (
                            -fractional_sum - sum(lower_bounds)
                        )
                        base_choices = bounded_triple_count(
                            lengths, base_total
                        )
                        three_mixed += (
                            high_bit_choices
                            * low_bit_choices
                            * base_choices
                        )

        next0 = [0] * (u + 1)
        next1 = [0] * (u + 1)
        next0[0] = 3 * carry0[0]
        next1[0] = carry0[0]
        for carry_ones in range(1, u):
            next0[carry_ones] = (
                3 * carry0[carry_ones]
                + carry1[carry_ones - 1]
            )
            next1[carry_ones] = (
                carry0[carry_ones]
                + 3 * carry1[carry_ones - 1]
            )
        next0[u] = carry1[u - 1]
        next1[u] = 3 * carry1[u - 1]
        carry0, carry1 = next0, next1

    return all_monochrome + two_mixed + three_mixed


def count_modulo(m: int, modulus: int) -> int:
    inverse_two = pow(2, -1, modulus)

    powers_two = [1] * (m + 1)
    inverse_powers_two = [1] * (m + 1)
    for exponent in range(1, m + 1):
        powers_two[exponent] = (
            2 * powers_two[exponent - 1]
        ) % modulus
        inverse_powers_two[exponent] = (
            inverse_two * inverse_powers_two[exponent - 1]
        ) % modulus

    # Prefix moments sum a^degree / 2^a, for degree 0, 1, 2.
    moments = [[0] * (m + 1) for _ in range(3)]
    for a in range(1, m + 1):
        weight = inverse_powers_two[a]
        moments[0][a] = (moments[0][a - 1] + weight) % modulus
        moments[1][a] = (
            moments[1][a - 1] + a * weight
        ) % modulus
        moments[2][a] = (
            moments[2][a - 1] + a * a * weight
        ) % modulus

    def interval_moments(
        lower: int, upper: int
    ) -> tuple[int, int, int]:
        if lower > upper:
            return 0, 0, 0
        return tuple(
            (prefix[upper] - prefix[lower - 1]) % modulus
            for prefix in moments
        )

    def weighted_unbounded_sum(
        slope: int,
        intercept: int,
        lower: int,
        upper: int,
    ) -> int:
        """Sum C(slope*a+intercept+2, 2) / 2**a."""
        if lower > upper:
            return 0
        moment0, moment1, moment2 = interval_moments(
            lower, upper
        )
        slope_mod = slope % modulus
        intercept_mod = intercept % modulus
        coefficient2 = slope_mod * slope_mod % modulus
        coefficient1 = (
            slope_mod * (2 * intercept_mod + 3)
        ) % modulus
        coefficient0 = (
            intercept_mod * intercept_mod
            + 3 * intercept_mod
            + 2
        ) % modulus
        return (
            inverse_two
            * (
                coefficient2 * moment2
                + coefficient1 * moment1
                + coefficient0 * moment0
            )
        ) % modulus

    choose_two = (1, 2, 1)

    def weighted_bounded_sum(
        b: int,
        fractional_sum: int,
        negative_a: int,
        negative_b: int,
    ) -> int:
        """Weighted bounded count for lengths (a,a,b), 1 <= a < b."""
        answer = 0
        for excluded_a in range(3):
            multiplicity = choose_two[excluded_a]
            for excluded_b in range(2):
                sign = (
                    -1
                    if (excluded_a + excluded_b) % 2
                    else 1
                )
                slope = negative_a - excluded_a
                intercept = (
                    (negative_b - excluded_b) * b
                    - fractional_sum
                )

                if slope == 0:
                    if intercept < 0:
                        continue
                    lower, upper = 1, b - 1
                elif slope > 0:
                    lower = max(1, ceil_div(-intercept, slope))
                    upper = b - 1
                else:
                    lower = 1
                    upper = min(b - 1, intercept // -slope)
                if lower > upper:
                    continue

                answer += (
                    sign
                    * multiplicity
                    * weighted_unbounded_sum(
                        slope, intercept, lower, upper
                    )
                )
        return answer % modulus

    def base_weights(
        b: int, fractional_sum: int
    ) -> list[int]:
        """Sum over T and group bases by silver-starting stack count."""
        weighted = [
            [
                weighted_bounded_sum(
                    b, fractional_sum, negative_a, negative_b
                )
                for negative_b in range(2)
            ]
            for negative_a in range(3)
        ]

        result = [0, 0, 0, 0]
        for negative_count in range(4):
            total = 0
            for negative_b in range(2):
                negative_a = negative_count - negative_b
                if 0 <= negative_a <= 2:
                    # Three placements of the short-denominator stack.
                    multiplicity = 3 * choose_two[negative_a]
                    total += (
                        multiplicity
                        * weighted[negative_a][negative_b]
                    )
            result[negative_count] = (
                total * powers_two[b - 1]
            ) % modulus
        return result

    all_monochrome = 3 * m * (m - 1) % modulus

    two_mixed = 0
    for exponent in range(1, m):
        initial_run_choices = m - exponent
        two_mixed += (
            powers_two[exponent - 1]
            * initial_run_choices
            * (initial_run_choices - 1)
        )
        two_mixed %= modulus
    two_mixed = 6 * two_mixed % modulus

    three_mixed = 0
    carry0 = [1]
    carry1 = [1]

    for u in range(1, m - 1):
        b = m - u
        bases_for_one = base_weights(b, 1)
        bases_for_two = base_weights(b, 2)

        for fractional_sum, final_carry, bases in (
            (1, 0, bases_for_one),
            (2, 1, bases_for_two),
        ):
            for negative_count in range(1, 4):
                numerator = (
                    fractional_sum
                    - negative_count
                    + u
                    + 1
                    - 4 * final_carry
                )
                if numerator % 2:
                    continue
                carry_ones = numerator // 2
                if not 0 <= carry_ones < u:
                    continue
                high_bit_choices = (
                    carry0[carry_ones]
                    if final_carry == 0
                    else carry1[carry_ones]
                )
                three_mixed += (
                    high_bit_choices * bases[negative_count]
                )
                three_mixed %= modulus

        next0 = [0] * (u + 1)
        next1 = [0] * (u + 1)
        next0[0] = 3 * carry0[0] % modulus
        next1[0] = carry0[0]
        for carry_ones in range(1, u):
            next0[carry_ones] = (
                3 * carry0[carry_ones]
                + carry1[carry_ones - 1]
            ) % modulus
            next1[carry_ones] = (
                carry0[carry_ones]
                + 3 * carry1[carry_ones - 1]
            ) % modulus
        next0[u] = carry1[u - 1]
        next1[u] = 3 * carry1[u - 1] % modulus
        carry0, carry1 = next0, next1

    return (
        all_monochrome + two_mixed + three_mixed
    ) % modulus


def solve() -> int:
    assert count_exact(2) == 6
    assert count_exact(5) == 348
    assert count_exact(20) == 125_825_982_708
    return count_modulo(TARGET, MODULUS)


if __name__ == "__main__":
    print(solve())
