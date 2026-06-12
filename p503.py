#!/usr/bin/env python3


def F(cards):
    continuation = float("inf")
    for seen in range(cards - 1, -1, -1):
        ranks = seen + 1
        scale = (cards + 1) / (seen + 2)

        if continuation == float("inf"):
            stop_count = ranks
        else:
            stop_count = int(continuation / scale)
            if stop_count < 0:
                stop_count = 0
            elif stop_count > ranks:
                stop_count = ranks

        stop_sum = scale * stop_count * (stop_count + 1) / 2
        continue_sum = (ranks - stop_count) * (
            0 if continuation == float("inf") else continuation
        )
        continuation = (stop_sum + continue_sum) / ranks

    return continuation


def solve():
    assert abs(F(3) - 5 / 3) < 1e-12
    assert abs(F(4) - 15 / 8) < 1e-12
    assert f"{F(10):.10f}" == "2.5579365079"
    return f"{F(1_000_000):.10f}"


if __name__ == "__main__":
    print(solve())
