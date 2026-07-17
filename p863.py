#!/usr/bin/env python3
"""Project Euler 863: optimal predetermined sequences of different dice."""


ITERATIONS = 30


def optimal_rolls(target_sides: int, iterations: int = ITERATIONS) -> float:
    """Return the minimum expected rolls for a target die."""
    # If r unresolved equiprobable states remain, rolling a d-sided die
    # leaves (d*r mod n) rejected states.  For W(r)=r*V(r), Bellman's
    # equation is
    #
    # W(r) = r + min(W(5r mod n)/5, W(6r mod n)/6).
    #
    # This operator contracts by at least a factor of five, so 30 iterations
    # are ample for the requested six decimal places.
    values = [0.0] * target_sides
    for _ in range(iterations):
        previous = values
        values = [0.0] + [
            remainder
            + min(
                previous[(5 * remainder) % target_sides] / 5.0,
                previous[(6 * remainder) % target_sides] / 6.0,
            )
            for remainder in range(1, target_sides)
        ]
    return values[1]


def roll_sum(limit: int, iterations: int = ITERATIONS) -> float:
    return sum(
        optimal_rolls(sides, iterations)
        for sides in range(2, limit + 1)
    )


def solve() -> str:
    assert abs(optimal_rolls(8) - 2.083333333333333) < 1e-12
    assert f"{roll_sum(30):.6f}" == "56.054622"
    return f"{roll_sum(1_000):.6f}"


if __name__ == "__main__":
    print(solve())
