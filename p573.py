#!/usr/bin/env python3
import math


def E(n):
    log_factorial_n = math.lgamma(n + 1)
    total = 0.0

    for k in range(1, n + 1):
        if k == n:
            total += 1.0
            continue

        p = k / n
        log_term = (
            log_factorial_n
            - math.lgamma(k + 1)
            - math.lgamma(n - k + 1)
            + k * math.log(p)
            + (n - k) * math.log1p(-p)
        )
        total += math.exp(log_term)

    return total


def solve():
    assert abs(E(3) - 17 / 9) < 1e-12
    assert f"{E(4):.5f}" == "2.21875"
    assert f"{E(5):.4f}" == "2.5104"
    assert f"{E(10):.8f}" == "3.66021568"
    return f"{E(1_000_000):.4f}"


if __name__ == "__main__":
    print(solve())
