"""Project Euler Problem 925: Next Permutations of Squares.

Start with sum(n^2), then add B(n^2)-n^2.  Reading square digits from right
to left, that adjustment is fixed as soon as the first ascent is found.

Only nonincreasing square suffixes need to be retained.  Up to 16 digits,
their root counts modulo 10^k follow directly from 2- and 5-adic valuations.
Beyond 16 digits, roots are represented by at most eight CRT progressions
below 10^16 and are lifted one digit at a time.  Just four fully
nonincreasing squares survive all 32 digits.
"""

from functools import cache
from math import isqrt


MODULUS = 1_000_000_007
LIMIT = 10**16
INPUT_DIGITS = 16
SQUARE_DIGITS = 32
POWERS_TWO = [2**exponent for exponent in range(SQUARE_DIGITS + 1)]
POWERS_FIVE = [5**exponent for exponent in range(SQUARE_DIGITS + 1)]

PrimeComponent = tuple[int, tuple[int, ...]]
RichState = tuple[int, PrimeComponent, PrimeComponent]


def prime_power_root_count(value: int, prime: int, exponent: int) -> int:
    powers = POWERS_TWO if prime == 2 else POWERS_FIVE
    modulus = powers[exponent]
    if value % modulus == 0:
        return prime ** (exponent // 2)

    unit = value
    valuation = 0
    while unit % prime == 0:
        unit //= prime
        valuation += 1
    if valuation & 1:
        return 0

    half_valuation = valuation // 2
    unit_exponent = exponent - 2 * half_valuation
    if prime == 5:
        unit_roots = 2 if unit % 5 in (1, 4) else 0
    elif unit_exponent == 1:
        unit_roots = 1
    elif unit_exponent == 2:
        unit_roots = 2 if unit % 4 == 1 else 0
    else:
        unit_roots = 4 if unit % 8 == 1 else 0
    return unit_roots * prime**half_valuation


def unit_square_roots(unit: int, prime: int, exponent: int) -> list[int]:
    powers = POWERS_TWO if prime == 2 else POWERS_FIVE
    unit %= powers[exponent]

    if prime == 5:
        roots = [root for root in range(5) if root * root % 5 == unit % 5]
        modulus = 5
        for _ in range(2, exponent + 1):
            next_modulus = modulus * 5
            target = unit % next_modulus
            roots = [
                root + digit * modulus
                for root in roots
                for digit in range(5)
                if (root + digit * modulus) ** 2 % next_modulus == target
            ]
            modulus = next_modulus
        return roots

    if exponent == 1:
        return [1]
    if exponent == 2:
        return [root for root in (1, 3) if root * root % 4 == unit % 4]

    roots = [root for root in (1, 3, 5, 7) if root * root % 8 == unit % 8]
    modulus = 8
    for _ in range(4, exponent + 1):
        next_modulus = modulus * 2
        target = unit % next_modulus
        roots = [
            root + digit * modulus
            for root in roots
            for digit in (0, 1)
            if (root + digit * modulus) ** 2 % next_modulus == target
        ]
        modulus = next_modulus
    return roots


def prime_component(
    value: int,
    prime: int,
    exponent: int,
) -> PrimeComponent:
    """Represent roots as base residues modulo a prime-power step."""
    powers = POWERS_TWO if prime == 2 else POWERS_FIVE
    modulus = powers[exponent]
    if value % modulus == 0:
        return powers[(exponent + 1) // 2], (0,)

    unit = value
    valuation = 0
    while unit % prime == 0:
        unit //= prime
        valuation += 1
    if valuation & 1:
        return 1, ()

    half_valuation = valuation // 2
    unit_exponent = exponent - 2 * half_valuation
    step = powers[exponent - half_valuation]
    scale = powers[half_valuation]
    roots = tuple(
        scale * root % step
        for root in unit_square_roots(unit, prime, unit_exponent)
    )
    return step, roots


def lift_component(
    value: int,
    child: int,
    prime: int,
    exponent: int,
    component: PrimeComponent,
) -> PrimeComponent:
    powers = POWERS_TWO if prime == 2 else POWERS_FIVE
    if value % powers[exponent] == 0:
        return prime_component(child, prime, exponent + 1)

    step, roots = component
    next_step = step * prime
    next_modulus = powers[exponent + 1]
    target = child % next_modulus
    lifted = tuple(
        candidate
        for root in roots
        for digit in range(prime)
        for candidate in (root + digit * step,)
        if candidate * candidate % next_modulus == target
    )
    return next_step, lifted


@cache
def crt_inverse(power_two: int, power_five: int) -> int:
    return pow(power_two, -1, power_five)


def crt_classes(
    two_component: PrimeComponent,
    five_component: PrimeComponent,
) -> tuple[int, tuple[int, ...]]:
    power_two, roots_two = two_component
    power_five, roots_five = five_component
    if not roots_two or not roots_five:
        return 1, ()

    inverse = crt_inverse(power_two, power_five)
    step = power_two * power_five
    residues = tuple(
        {
            (
                root_two
                + power_two
                * ((root_five - root_two) * inverse % power_five)
            )
            % step
            for root_two in roots_two
            for root_five in roots_five
        }
    )
    return step, residues


def bounded_root_count(
    two_component: PrimeComponent,
    five_component: PrimeComponent,
) -> int:
    step, residues = crt_classes(two_component, five_component)
    return sum(
        LIMIT // step
        if residue == 0
        else (LIMIT - residue) // step + 1
        if residue <= LIMIT
        else 0
        for residue in residues
    )


def permutation_adjustment(value: int, width: int) -> int:
    digits = list(f"{value:0{width}d}")
    pivot = width - 2
    while pivot >= 0 and digits[pivot] >= digits[pivot + 1]:
        pivot -= 1
    assert pivot >= 0

    successor = width - 1
    while digits[successor] <= digits[pivot]:
        successor -= 1
    digits[pivot], digits[successor] = digits[successor], digits[pivot]
    digits[pivot + 1 :] = reversed(digits[pivot + 1 :])
    return int("".join(digits)) - value


def add_finalized_adjustment(
    total: int,
    parent: int,
    child: int,
    prepended_digit: int,
    width: int,
    root_count: int,
) -> int:
    adjustment = permutation_adjustment(child, width)
    contribution = root_count * adjustment

    # A prepended zero is not a real digit when parent is the complete square.
    # Such a globally nonincreasing square has B(parent)=0.
    if prepended_digit == 0 and parent:
        root = isqrt(parent)
        if root * root == parent:
            contribution -= parent + adjustment

    return (total + contribution) % MODULUS


def square_permutation_sum() -> int:
    states = [
        digit
        for digit in range(10)
        if prime_power_root_count(digit, 2, 1)
        * prime_power_root_count(digit, 5, 1)
    ]
    decimal_power = 10
    adjustment_sum = 0

    # Cheap uniform root counts while 10^width divides the complete input
    # interval length.
    for width_minus_one in range(1, INPUT_DIGITS):
        width = width_minus_one + 1
        next_states = []
        for suffix in states:
            leading_digit = suffix // (decimal_power // 10)
            for digit in range(10):
                child = digit * decimal_power + suffix
                root_count = (
                    prime_power_root_count(child, 2, width)
                    * prime_power_root_count(child, 5, width)
                    * 10 ** (INPUT_DIGITS - width)
                )
                if not root_count:
                    continue
                if digit < leading_digit:
                    adjustment_sum = add_finalized_adjustment(
                        adjustment_sum,
                        suffix,
                        child,
                        digit,
                        width,
                        root_count,
                    )
                else:
                    next_states.append(child)
        states = next_states
        decimal_power *= 10

    rich_states: list[RichState] = [
        (
            suffix,
            prime_component(suffix, 2, INPUT_DIGITS),
            prime_component(suffix, 5, INPUT_DIGITS),
        )
        for suffix in states
    ]

    # Above 16 digits, carry and lift the actual CRT root progressions.
    for width_minus_one in range(INPUT_DIGITS, SQUARE_DIGITS):
        width = width_minus_one + 1
        next_states: list[RichState] = []
        for suffix, two_component, five_component in rich_states:
            leading_digit = suffix // (decimal_power // 10)
            for digit in range(10):
                child = digit * decimal_power + suffix
                next_two = lift_component(
                    suffix,
                    child,
                    2,
                    width_minus_one,
                    two_component,
                )
                next_five = lift_component(
                    suffix,
                    child,
                    5,
                    width_minus_one,
                    five_component,
                )
                root_count = bounded_root_count(next_two, next_five)
                if not root_count:
                    continue
                if digit < leading_digit:
                    adjustment_sum = add_finalized_adjustment(
                        adjustment_sum,
                        suffix,
                        child,
                        digit,
                        width,
                        root_count,
                    )
                else:
                    next_states.append((child, next_two, next_five))
        rich_states = next_states
        decimal_power *= 10

    # Remaining exact squares have globally nonincreasing digits, hence B=0.
    for _, two_component, five_component in rich_states:
        step, residues = crt_classes(two_component, five_component)
        for residue in residues:
            number = step if residue == 0 else residue
            while number <= LIMIT:
                adjustment_sum = (adjustment_sum - number * number) % MODULUS
                number += step

    square_sum = (
        (LIMIT % MODULUS)
        * ((LIMIT + 1) % MODULUS)
        * ((2 * LIMIT + 1) % MODULUS)
        * pow(6, MODULUS - 2, MODULUS)
    ) % MODULUS
    return (square_sum + adjustment_sum) % MODULUS


def exact_next_permutation(value: int) -> int:
    digits = list(str(value))
    pivot = len(digits) - 2
    while pivot >= 0 and digits[pivot] >= digits[pivot + 1]:
        pivot -= 1
    if pivot < 0:
        return 0
    successor = len(digits) - 1
    while digits[successor] <= digits[pivot]:
        successor -= 1
    digits[pivot], digits[successor] = digits[successor], digits[pivot]
    digits[pivot + 1 :] = reversed(digits[pivot + 1 :])
    return int("".join(digits))


def brute_sum(limit: int) -> int:
    return sum(exact_next_permutation(number * number) for number in range(1, limit + 1))


def solve() -> int:
    assert brute_sum(10) == 270
    assert brute_sum(100) == 335_316
    return square_permutation_sum()


if __name__ == "__main__":
    print(solve())
