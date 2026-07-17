#!/usr/bin/env python3
"""Project Euler 859: count cookie partitions won by Even."""


LIMIT = 300


def pile_values(limit: int) -> list[int]:
    """Return the integer partizan-game value of every pile size."""
    values = [0] * (limit + 1)
    for size in range(1, limit + 1):
        if size % 2:
            child_sum = 2 * values[(size - 1) // 2]
            # The game is {child_sum |}.  Zero is the simplest number above
            # a negative option; otherwise the next integer is required.
            values[size] = child_sum + 1 if child_sum >= 0 else 0
        else:
            child_sum = 2 * values[(size - 2) // 2]
            # Dually, this game is {| child_sum}.
            values[size] = child_sum - 1 if child_sum <= 0 else 0
    return values


def even_winning_partitions(total_cookies: int) -> int:
    """Count partitions whose summed game value is non-positive."""
    values = pile_values(total_cookies)
    offset = total_cookies
    counts = [
        [0] * (2 * total_cookies + 1)
        for _ in range(total_cookies + 1)
    ]
    counts[0][offset] = 1

    # Standard unbounded-partition DP, augmented by the additive game value.
    for pile_size in range(1, total_cookies + 1):
        value_shift = values[pile_size]
        for cookie_count in range(pile_size, total_cookies + 1):
            source = counts[cookie_count - pile_size]
            destination = counts[cookie_count]
            source_bound = cookie_count - pile_size
            for game_value in range(-source_bound, source_bound + 1):
                ways = source[game_value + offset]
                if ways:
                    destination[
                        game_value + value_shift + offset
                    ] += ways

    # A negative value is an Even win; zero is a loss for the first player,
    # Odd, and is therefore also an Even win.
    return sum(counts[total_cookies][: offset + 1])


def solve() -> int:
    assert even_winning_partitions(5) == 2
    assert even_winning_partitions(16) == 64
    return even_winning_partitions(LIMIT)


if __name__ == "__main__":
    print(solve())
