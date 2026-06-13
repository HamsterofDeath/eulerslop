#!/usr/bin/env python3
"""Project Euler 629: Scatterstone Nim."""

MOD = 1_000_000_007
N = 200


def grundy_for_three_splits(limit):
    """Single-pile Grundy values when each move may split into 2 or 3 piles."""
    grundy = [0] * (limit + 1)
    for n in range(2, limit + 1):
        seen = set()

        for a in range(1, n // 2 + 1):
            seen.add(grundy[a] ^ grundy[n - a])

        for a in range(1, n // 3 + 1):
            remainder = n - a
            for b in range(a, remainder // 2 + 1):
                seen.add(grundy[a] ^ grundy[b] ^ grundy[remainder - b])

        g = 0
        while g in seen:
            g += 1
        grundy[n] = g
    return grundy


def losing_partitions(limit, labels):
    """Count partitions of limit whose part labels xor to zero."""
    width = 1 << max(1, max(labels).bit_length())
    dp = [[0] * width for _ in range(limit + 1)]
    dp[0][0] = 1

    for part in range(1, limit + 1):
        label = labels[part]
        for total in range(part, limit + 1):
            previous = dp[total - part]
            current = dp[total]
            for xor_value, count in enumerate(previous):
                if count:
                    target = xor_value ^ label
                    current[target] = (current[target] + count) % MOD

    return dp[limit][0], sum(dp[limit]) % MOD


def solve(n=N):
    # k = 2: a heap is equivalent to 1 exactly when its size is even.
    losing_k2, total_partitions = losing_partitions(
        n, [0] + [1 if size % 2 == 0 else 0 for size in range(1, n + 1)]
    )

    # k = 3 has no similarly compact pattern at this size, but direct mex is tiny.
    losing_k3, _ = losing_partitions(n, grundy_for_three_splits(n))

    # For k >= 4, induction gives G(heap size s) = s - 1.
    losing_k4_plus, _ = losing_partitions(n, [0] + [size - 1 for size in range(1, n + 1)])

    winning_k2 = total_partitions - losing_k2
    winning_k3 = total_partitions - losing_k3
    winning_k4_plus = total_partitions - losing_k4_plus

    return (winning_k2 + winning_k3 + (n - 3) * winning_k4_plus) % MOD


if __name__ == "__main__":
    print(solve())
