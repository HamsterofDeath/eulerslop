#!/usr/bin/env python3
"""Project Euler Problem 978: Random Walk Skewness.

With X_t=X_(t-1)+epsilon*abs(X_(t-2)), odd powers of the independent
random sign epsilon vanish.  The raw second and third moments therefore
satisfy

    A_t = A_(t-1) + A_(t-2),
    B_t = B_(t-1) + 3*B_(t-2),

both starting with values 0,1.  The mean is one, so the variance is
A_t-1 and the central third moment is B_t-3*A_t+2.
"""

from decimal import Decimal, localcontext


TARGET_TIME = 50


def moments(time: int) -> tuple[int, int]:
    second_previous, second = 0, 1
    third_previous, third = 0, 1
    for _ in range(2, time + 1):
        second_previous, second = (
            second,
            second + second_previous,
        )
        third_previous, third = (
            third,
            third + 3 * third_previous,
        )
    return second, third


def skewness(time: int) -> Decimal:
    second, third = moments(time)
    variance = second - 1
    central_third = third - 3 * second + 2
    with localcontext() as context:
        context.prec = 50
        return Decimal(central_third) / (
            Decimal(variance).sqrt() ** 3
        )


def solve() -> str:
    assert skewness(5) == Decimal("0.75")
    assert f"{skewness(10):.8f}" == "2.50997097"
    return f"{skewness(TARGET_TIME):.8f}"


if __name__ == "__main__":
    print(solve())
