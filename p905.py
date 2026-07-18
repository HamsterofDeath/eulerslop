#!/usr/bin/env python3
"""Project Euler 905: the three epistemologists."""


def turns_until_known(a: int, b: int, c: int) -> int:
    """Return F(a,b,c).

    A player who sees x and y considers only the two possible values
    x+y and |x-y| (the latter is absent when x=y).  Consequently the
    worlds form a rooted tree.  Its roots are permutations of
    (g,g,2g), where the player wearing 2g knows immediately.  Away from
    a root, only the player wearing the sum can know: their alternative
    world is the parent obtained by replacing the sum by the difference.

    Moving to a parent is exactly one subtractive Euclidean step on the
    two smaller values.  Consecutive subtractions by the same smaller
    value alternate the labels of the largest hat, so an entire Euclidean
    quotient can be processed at once.
    """
    values = [a, b, c]
    largest = max(range(3), key=values.__getitem__)
    elapsed = 0

    while True:
        other = [index for index in range(3) if index != largest]
        if values[other[0]] == values[other[1]]:
            # This largest-hat player knows on their first scheduled turn.
            return elapsed + largest + 1

        if values[other[0]] > values[other[1]]:
            large, small = other
        else:
            large, small = other[1], other[0]

        large_value = values[large]
        small_value = values[small]

        # Stop at equality rather than taking a final subtraction to zero.
        quotient = (large_value - 1) // small_value
        remainder = large_value - quotient * small_value

        # Largest labels alternate: largest, large, largest, large, ...
        first_delay = (largest - large) % 3 or 3
        elapsed += 3 * (quotient // 2)
        if quotient & 1:
            elapsed += first_delay
            values[large] = small_value + remainder
            values[largest] = remainder
            largest = large
        else:
            values[largest] = small_value + remainder
            values[large] = remainder


def solve() -> int:
    assert turns_until_known(2, 1, 1) == 1
    assert turns_until_known(2, 7, 5) == 5

    answer = 0
    for a in range(1, 8):
        for b in range(1, 20):
            a_power_b = a**b
            b_power_a = b**a
            answer += turns_until_known(
                a_power_b,
                b_power_a,
                a_power_b + b_power_a,
            )
    return answer


if __name__ == "__main__":
    print(solve())
