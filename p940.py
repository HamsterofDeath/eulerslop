#!/usr/bin/env python3
"""Project Euler Problem 940: The Great Fibonacci Function.

Writing x_n=A(0,n), the defining recurrences imply

    x_(n+2) = x_(n+1) + 3*x_n
    A(m,n) = (1+E)**m x_n.

If alpha and beta are the roots of t**2-t-3, this gives

    A(m,n) = ((1+alpha)**m * alpha**n
              - (1+beta)**m * beta**n) / sqrt(13).

The double sum therefore factorizes into two Fibonacci-indexed power
sums, evaluated below in the quadratic ring modulo the target.
"""

MODULUS = 1_123_581_313
INVERSE_TWO = (MODULUS + 1) // 2

Quadratic = tuple[int, int]  # a + b*sqrt(13)


def multiply(left: Quadratic, right: Quadratic) -> Quadratic:
    a, b = left
    c, d = right
    return (
        (a * c + 13 * b * d) % MODULUS,
        (a * d + b * c) % MODULUS,
    )


def power(base: Quadratic, exponent: int) -> Quadratic:
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1
    return result


def add(left: Quadratic, right: Quadratic) -> Quadratic:
    return (
        (left[0] + right[0]) % MODULUS,
        (left[1] + right[1]) % MODULUS,
    )


def fibonacci_function_sum(maximum_index: int) -> int:
    fibonacci = [0, 1]
    for _ in range(2, maximum_index + 1):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

    alpha = (INVERSE_TWO, INVERSE_TWO)
    one_plus_alpha = (
        3 * INVERSE_TWO % MODULUS,
        INVERSE_TWO,
    )
    alpha_sum = (0, 0)
    shifted_sum = (0, 0)
    for index in range(2, maximum_index + 1):
        exponent = fibonacci[index]
        alpha_sum = add(alpha_sum, power(alpha, exponent))
        shifted_sum = add(
            shifted_sum,
            power(one_plus_alpha, exponent),
        )

    # Z - conjugate(Z), divided by sqrt(13), is twice
    # the sqrt(13) coefficient of Z.
    product = multiply(alpha_sum, shifted_sum)
    return 2 * product[1] % MODULUS


def solve() -> int:
    assert fibonacci_function_sum(3) == 30
    assert fibonacci_function_sum(5) == 10_396
    return fibonacci_function_sum(50)


if __name__ == "__main__":
    print(solve())
