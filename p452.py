#!/usr/bin/env python3

MOD = 1_234_567_891


def ordered_nonunit_counts(limit):
    """H[k] = ordered k-tuples of integers > 1 with product <= limit."""
    max_k = limit.bit_length() - 1

    values = []
    i = 1
    while i <= limit:
        q = limit // i
        values.append(q)
        i = limit // q + 1
    values.sort()
    index = {v: i for i, v in enumerate(values)}

    previous = [1] * len(values)
    counts = [1]

    for _ in range(1, max_k + 1):
        current = [0] * len(values)
        for pos, value in enumerate(values):
            if value < 2:
                continue
            total = 0
            start = 2
            while start <= value:
                quotient = value // start
                end = value // quotient
                total += (end - start + 1) * previous[index[quotient]]
                start = end + 1
            current[pos] = total % MOD
        previous = current
        counts.append(previous[index[limit]])

    return counts


def F(m, n):
    total = 0
    choose = 1
    for k, count in enumerate(ordered_nonunit_counts(m)):
        if k:
            choose = choose * (n - k + 1) // k
        total = (total + (choose % MOD) * count) % MOD
    return total


def solve():
    assert F(10, 10) == 571
    assert F(10**6, 10**6) == 252_903_833
    return str(F(10**9, 10**9))


if __name__ == "__main__":
    print(solve())
