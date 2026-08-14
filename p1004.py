#!/usr/bin/env python3
"""Project Euler Problem 1004: Balanced Integer.

For a digit string the RSK correspondence maps the word to a pair of
tableaux whose common shape lam satisfies: first row length = longest
non-strictly increasing subsequence, number of rows = longest strictly
decreasing subsequence.  A balanced integer has those two equal.

The number of words over the ten digits with LDS <= a and LNDS <= b is

    sum over partitions lam with at most a rows and rows of length <= b
    of f_lam * s_lam(1^10),

where f_lam is the number of standard tableaux and s_lam(1^10) the
number of semistandard tableaux of shape lam over ten entries, both
given by hook products.  Since a balanced number has LNDS = LDS <= 10,
every digit appears at most 10 times and the length is at most 100.

Words beginning with the digit 0 are removed: prepending 0 raises the
LNDS by one and leaves the LDS unchanged.
"""

from math import factorial


def gen_partitions(maxrow: int, maxrows: int) -> list[tuple[int, ...]]:
    result = []

    def rec(rows: list[int]) -> None:
        result.append(tuple(rows))
        if len(rows) < maxrows and (rows[-1] if rows else maxrow) > 0:
            limit = rows[-1] if rows else maxrow
            for r in range(1, limit + 1):
                rec(rows + [r])

    rec([])
    return result


def hook_product(lam: tuple[int, ...]) -> int:
    product = 1
    for i, row in enumerate(lam, start=1):
        for j in range(1, row + 1):
            col = sum(1 for r in lam if r >= j)
            product *= row - j + col - i + 1
    return product


def word_counts() -> list[list[int]]:
    """W[a][b]: number of digit words (any length, leading zeros
    allowed) with LDS <= a and LNDS <= b."""
    w = [[0] * 11 for _ in range(11)]
    for lam in gen_partitions(10, 10):
        size = sum(lam)
        hooks = hook_product(lam)
        standard = factorial(size) // hooks
        content = 1
        for i, row in enumerate(lam, start=1):
            for j in range(1, row + 1):
                content *= 10 + j - i
        semistandard = content // hooks
        for a in range(len(lam), 11):
            for b in range(lam[0] if lam else 0, 11):
                w[a][b] += standard * semistandard
    return w


W = word_counts()


def D(a: int, b: int) -> int:
    """Positive numbers (no leading zero) with LDS <= a and LNDS <= b."""
    if a == 0:
        return 0
    return W[a][b] - 1 - (W[a][b - 1] if b >= 1 else 0)


def balanced_below(limit: int) -> int:
    """Balanced integers with at most `limit` digits, via per-length
    counts: a length-L word starting with 0 must drop its leading zero,
    so subtract words of length L-1 with LNDS <= b-1."""
    per_length = []
    for lam in gen_partitions(10, 10):
        size = sum(lam)
        hooks = hook_product(lam)
        standard = factorial(size) // hooks
        content = 1
        for i, row in enumerate(lam, start=1):
            for j in range(1, row + 1):
                content *= 10 + j - i
        semistandard = content // hooks
        per_length.append((size, len(lam), lam[0] if lam else 0,
                           standard * semistandard))
    total = 0
    for length in range(1, limit + 1):
        w = [[[0] * 11 for _ in range(11)] for _ in range(2)]
        for size, rows, first, ways in per_length:
            if size != length:
                continue
            for a in range(rows, 11):
                for b in range(first, 11):
                    w[0][a][b] += ways
        for size, rows, first, ways in per_length:
            if size != length - 1:
                continue
            for a in range(rows, 11):
                for b in range(first, 11):
                    w[1][a][b] += ways
        for k in range(1, 11):
            def d(a: int, b: int) -> int:
                if a == 0 or b < 0:
                    return 0
                return w[0][a][b] - (w[1][a][b - 1] if b >= 1 else 0)
            total += d(k, k) - d(k - 1, k) - d(k, k - 1) + d(k - 1, k - 1)
    return total


def solve() -> int:
    total = sum(
        D(k, k) - D(k - 1, k) - D(k, k - 1) + D(k - 1, k - 1)
        for k in range(1, 11)
    )
    return total % 1_000_000_007


if __name__ == "__main__":
    assert balanced_below(4) == 2274
    print(solve())
