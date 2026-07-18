"""Project Euler Problem 923: Young's Game with Unit Moves.

Unit moves turn an (a,b,k)-staircase into either an integer or a hot switch.
Let n be the first positive integer with floor(n/a)+floor(n/b) >= k.

* If n is a simultaneous a- and b-milestone and the sum reaches exactly k,
  the game is the switch {b-1 | -(a-1)}.
* Otherwise it is the integer
  (b-(n-1) mod b) - (a-(n-1) mod a).

In a sum, switches are played in decreasing temperature a+b-2. Within one
temperature group, the total contribution is independent of play order.
A bounded dynamic program tracks selected components, whose turn reaches the
next temperature group, and the accumulated integer score.
"""

from collections import defaultdict
from math import comb, gcd


MODULUS = 1_000_000_007
TARGET_DIAGRAMS = 8
TARGET_WEIGHT = 64


def classify_staircases(
    weight_limit: int,
) -> tuple[dict[int, int], dict[int, dict[int, int]]]:
    """Return integer multiplicities and switch counts grouped by a+b and b."""
    integers: dict[int, int] = defaultdict(int)
    switches: dict[int, dict[int, int]] = {}

    for a in range(1, weight_limit - 1):
        for b in range(1, weight_limit - a):
            side_sum = a + b
            milestone_period = side_sum // gcd(a, b)

            for k in range(1, weight_limit - side_sum + 1):
                if k % milestone_period == 0:
                    switches.setdefault(side_sum, defaultdict(int))[b] += 1
                    continue

                lower = 0
                upper = max(a, b) * k
                while lower + 1 < upper:
                    middle = (lower + upper) // 2
                    if middle // a + middle // b >= k:
                        upper = middle
                    else:
                        lower = middle

                milestone = upper
                down_distance = a - (milestone - 1) % a
                right_distance = b - (milestone - 1) % b
                integers[right_distance - down_distance] += 1

    assert sum(integers.values()) + sum(
        sum(group.values()) for group in switches.values()
    ) == comb(weight_limit, 3)
    return integers, switches


def ordered_sum_powers(
    multiplicities: dict[int, int],
    maximum_count: int,
) -> list[dict[int, int]]:
    """Distributions of sums of r ordered draws, for 0 <= r <= maximum."""
    powers: list[dict[int, int]] = [{0: 1}]

    for _ in range(maximum_count):
        next_power: dict[int, int] = defaultdict(int)
        for current_sum, ways in powers[-1].items():
            for value, multiplicity in multiplicities.items():
                next_sum = current_sum + value
                next_power[next_sum] = (
                    next_power[next_sum] + ways * multiplicity
                ) % MODULUS
        powers.append(next_power)

    return powers


def right_winning_tuples(diagram_count: int, weight_limit: int) -> int:
    integers, switch_groups = classify_staircases(weight_limit)

    # State: (selected count, turn parity, accumulated score) -> ways.
    # Parity zero means Right (the horizontal player) reaches the next group.
    states = {(0, 0, 0): 1}

    for side_sum, group in sorted(switch_groups.items(), reverse=True):
        group_powers = ordered_sum_powers(group, diagram_count)
        next_states: dict[tuple[int, int, int], int] = defaultdict(int)

        for (selected, parity, score), ways in states.items():
            for count in range(diagram_count - selected + 1):
                if parity == 0:
                    right_moves = (count + 1) // 2
                else:
                    right_moves = count // 2
                down_moves = count - right_moves

                constant = -right_moves - down_moves * (side_sum - 1)
                interleavings = comb(selected + count, count)

                for b_sum, group_ways in group_powers[count].items():
                    key = (
                        selected + count,
                        parity ^ (count & 1),
                        score + b_sum + constant,
                    )
                    next_states[key] = (
                        next_states[key]
                        + ways * group_ways * interleavings
                    ) % MODULUS

        states = next_states

    integer_powers = ordered_sum_powers(integers, diagram_count)
    answer = 0

    for (switch_count, parity, switch_score), ways in states.items():
        integer_count = diagram_count - switch_count
        interleavings = comb(diagram_count, integer_count)

        for integer_score, integer_ways in integer_powers[
            integer_count
        ].items():
            score = switch_score + integer_score
            if score > 0 or (score == 0 and parity == 1):
                answer = (
                    answer
                    + ways * integer_ways * interleavings
                ) % MODULUS

    return answer


def solve() -> int:
    assert right_winning_tuples(2, 4) == 7
    assert right_winning_tuples(3, 9) == 315_319
    return right_winning_tuples(TARGET_DIAGRAMS, TARGET_WEIGHT)


if __name__ == "__main__":
    print(solve())
