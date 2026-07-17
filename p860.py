#!/usr/bin/env python3
"""Project Euler 860: fair arrangements of two-coin stacks."""


STACKS = 9_898
MODULUS = 989_898_989


def fair_arrangements(stack_count: int, modulus: int = MODULUS) -> int:
    """Return F(stack_count) modulo the given prime modulus."""
    # The four stack types GG, GS, SG, SS have partizan number values
    # 2, 1/2, -1/2, -2.  After doubling, fair arrangements are the central
    # coefficient of (x^4 + x + x^-1 + x^-4)^n.
    #
    # Factoring this as
    # (x^(5/2)+x^(-5/2)) (x^(3/2)+x^(-3/2))
    # makes the central-exponent condition 5*j + 3*k = 4*n.
    factorials = [1] * (stack_count + 1)
    for value in range(1, stack_count + 1):
        factorials[value] = factorials[value - 1] * value % modulus

    inverse_factorials = [1] * (stack_count + 1)
    inverse_factorials[stack_count] = pow(
        factorials[stack_count], modulus - 2, modulus
    )
    for value in range(stack_count, 0, -1):
        inverse_factorials[value - 1] = (
            inverse_factorials[value] * value
        ) % modulus

    def choose(selected: int) -> int:
        return (
            factorials[stack_count]
            * inverse_factorials[selected]
            % modulus
            * inverse_factorials[stack_count - selected]
            % modulus
        )

    result = 0
    for first_selected in range(stack_count + 1):
        remainder = 4 * stack_count - 5 * first_selected
        if remainder % 3:
            continue
        second_selected = remainder // 3
        if 0 <= second_selected <= stack_count:
            result += choose(first_selected) * choose(second_selected)
            result %= modulus
    return result


def solve() -> int:
    assert fair_arrangements(2) == 4
    assert fair_arrangements(10) == 63_594
    return fair_arrangements(STACKS)


if __name__ == "__main__":
    print(solve())
