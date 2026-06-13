#!/usr/bin/env python3
"""Project Euler 732: trolls escaping a hole."""


MODULUS = 1_000_000_007
TARGET = 1000


def trolls(count: int) -> list[tuple[int, int, int]]:
    values = []
    power = 1
    for _ in range(3 * count):
        values.append(power % 101 + 50)
        power = power * 5 % MODULUS
    return [(values[3 * i], values[3 * i + 1], values[3 * i + 2]) for i in range(count)]


def q_value(count: int) -> int:
    data = trolls(count)
    total_height = sum(height for height, _, _ in data)
    total_height_squared = total_height * total_height
    data.sort(key=lambda item: item[0] + item[1])

    unreachable = -10**9
    dp = [unreachable] * (total_height + 151)
    dp[0] = 0
    largest_height = 0

    for height, arms, iq in data:
        for removed_height in range(largest_height, -1, -1):
            if dp[removed_height] == unreachable:
                continue
            reach = total_height - removed_height + arms
            if 2 * reach * reach < total_height_squared:
                continue
            next_height = removed_height + height
            dp[next_height] = max(dp[next_height], dp[removed_height] + iq)
            largest_height = max(largest_height, next_height)

    return max(dp)


def solve() -> int:
    assert q_value(5) == 401
    assert q_value(15) == 941
    return q_value(TARGET)


if __name__ == "__main__":
    print(solve())
