#!/usr/bin/env python3
"""Project Euler 901: optimal drilling depths."""

from decimal import Decimal, ROUND_HALF_UP, localcontext


def minimal_expected_time() -> Decimal:
    """Return the optimal expected drilling time.

    Let d_0=0 and let d_i be the increasing sequence of attempted
    depths.  Attempt i is reached with probability exp(-d_{i-1}), so

        E = sum_{i>=1} d_i exp(-d_{i-1}).

    Differentiating with respect to each interior d_i gives

        d_{i+1} = exp(d_i-d_{i-1}).

    All but one choice of d_1 eventually make this recurrence either
    decrease or grow explosively.  Bisection isolates the unique
    separating trajectory, which is the minimizing sequence.
    """
    with localcontext() as context:
        context.prec = 90

        def trajectory_side(first_depth: Decimal) -> int:
            previous = Decimal(0)
            current = first_depth
            for _ in range(200):
                following = (current - previous).exp()
                if following <= current:
                    return -1
                if current > 5 and following > 2 * current:
                    return 1
                previous, current = current, following
            raise ArithmeticError("trajectory did not leave the separator")

        low = Decimal("0.7")
        high = Decimal("0.8")
        assert trajectory_side(low) == -1
        assert trajectory_side(high) == 1

        for _ in range(320):
            midpoint = (low + high) / 2
            if midpoint == low or midpoint == high:
                break
            if trajectory_side(midpoint) < 0:
                low = midpoint
            else:
                high = midpoint

        first_depth = (low + high) / 2

        # The stationarity recurrence changes every term from the second
        # onward into d_i exp(-d_{i-1}) = exp(-d_{i-2}).
        expected_time = first_depth + Decimal(1)
        previous = Decimal(0)
        current = first_depth
        expected_time += (-current).exp()

        for _ in range(200):
            following = (current - previous).exp()
            if (
                following <= current
                or (current > 5 and following > 2 * current)
            ):
                break
            previous, current = current, following
            expected_time += (-current).exp()

        return +expected_time


def solve() -> str:
    answer = minimal_expected_time()
    assert Decimal("2.36449") < answer < Decimal("2.36450")
    return format(
        answer.quantize(
            Decimal("0.000000001"),
            rounding=ROUND_HALF_UP,
        ),
        "f",
    )


if __name__ == "__main__":
    print(solve())
