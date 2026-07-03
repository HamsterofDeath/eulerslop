#!/usr/bin/env python3
"""Project Euler 828: number challenges."""

from pathlib import Path


MOD = 1_005_075_251
DATA_FILE = Path(__file__).with_name("0828_number_challenges.txt")


def minimum_score(target: int, numbers: list[int]) -> int:
    count = len(numbers)
    values = [set() for _ in range(1 << count)]
    scores = [0] * (1 << count)

    for index, value in enumerate(numbers):
        values[1 << index].add(value)

    for mask in range(1, 1 << count):
        scores[mask] = sum(numbers[i] for i in range(count) if mask & (1 << i))
        submask = (mask - 1) & mask
        while submask:
            other = mask ^ submask
            if submask < other:
                for left in values[submask]:
                    for right in values[other]:
                        values[mask].add(left + right)
                        values[mask].add(left * right)
                        if left > right:
                            values[mask].add(left - right)
                        elif right > left:
                            values[mask].add(right - left)
                        if right and left % right == 0:
                            values[mask].add(left // right)
                        if left and right % left == 0:
                            values[mask].add(right // left)
            submask = (submask - 1) & mask

    best = 0
    for mask in range(1, 1 << count):
        if target in values[mask] and (best == 0 or scores[mask] < best):
            best = scores[mask]
    return best


def solve() -> int:
    total = 0
    power = 1
    scores = []
    for line in DATA_FILE.read_text().splitlines():
        target_text, numbers_text = line.split(":")
        target = int(target_text)
        numbers = [int(value) for value in numbers_text.split(",")]
        score = minimum_score(target, numbers)
        scores.append(score)
        power = power * 3 % MOD
        total = (total + power * score) % MOD

    assert len(scores) == 200
    assert scores[0] == 40
    return total


if __name__ == "__main__":
    print(solve())
