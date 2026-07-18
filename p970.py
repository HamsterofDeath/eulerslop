#!/usr/bin/env python3
"""Project Euler Problem 970: Kangaroo Hopping over Sixes.

The Laplace transform of H is 1/(s-1+exp(-s)).  The double pole at zero
contributes 2x+2/3.  Every other pole is

    q_k = 1 + W_k(-1/e)

and has residue exp(q_k*x)/q_k.  At x=10**6 the first conjugate pair
dominates all later pairs by hundreds of thousands of decimal places.
The code locates its upper-half-plane pole with Decimal complex Newton
iteration, scales the tiny correction close to unit decimal magnitude,
and extracts the requested non-six digits.
"""

from decimal import (
    Decimal,
    ROUND_FLOOR,
    localcontext,
)


LIMIT = 10**6


def arctangent(value: Decimal, epsilon: Decimal) -> Decimal:
    square = value * value
    term = value
    total = term
    denominator = 1
    while True:
        term *= -square
        denominator += 2
        addition = term / denominator
        total += addition
        if abs(addition) < epsilon:
            return total


def calculate_pi(epsilon: Decimal) -> Decimal:
    return (
        16 * arctangent(Decimal(1) / 5, epsilon)
        - 4 * arctangent(Decimal(1) / 239, epsilon)
    )


def sine_cosine(
    angle: Decimal,
    pi: Decimal,
    epsilon: Decimal,
) -> tuple[Decimal, Decimal]:
    two_pi = 2 * pi
    turns = (angle / two_pi).to_integral_value()
    angle -= turns * two_pi

    square = angle * angle
    sine_term = angle
    cosine_term = Decimal(1)
    sine = sine_term
    cosine = cosine_term

    index = 1
    while True:
        sine_term *= -square / ((2 * index) * (2 * index + 1))
        cosine_term *= -square / (
            (2 * index - 1) * (2 * index)
        )
        sine += sine_term
        cosine += cosine_term
        if abs(sine_term) < epsilon and abs(cosine_term) < epsilon:
            return sine, cosine
        index += 1


def complex_divide(
    numerator: tuple[Decimal, Decimal],
    denominator: tuple[Decimal, Decimal],
) -> tuple[Decimal, Decimal]:
    denominator_norm = (
        denominator[0] * denominator[0]
        + denominator[1] * denominator[1]
    )
    return (
        (
            numerator[0] * denominator[0]
            + numerator[1] * denominator[1]
        ) / denominator_norm,
        (
            numerator[1] * denominator[0]
            - numerator[0] * denominator[1]
        ) / denominator_norm,
    )


def dominant_pole(
    pi: Decimal,
    epsilon: Decimal,
) -> tuple[Decimal, Decimal]:
    real = Decimal("-2.1")
    imaginary = Decimal("7.5")

    for _ in range(30):
        sine, cosine = sine_cosine(imaginary, pi, epsilon)
        magnitude = (-real).exp()
        exponential = (magnitude * cosine, -magnitude * sine)
        function = (
            real - 1 + exponential[0],
            imaginary + exponential[1],
        )
        derivative = (
            1 - exponential[0],
            -exponential[1],
        )
        change = complex_divide(function, derivative)
        real -= change[0]
        imaginary -= change[1]
        if max(abs(change[0]), abs(change[1])) < epsilon:
            return real, imaginary
    raise AssertionError("complex Newton iteration did not converge")


def first_non_six_digits(
    fractional_part: Decimal,
    count: int = 8,
) -> str:
    result = []
    for _ in range(200):
        fractional_part *= 10
        digit = int(
            fractional_part.to_integral_value(rounding=ROUND_FLOOR)
        )
        fractional_part -= digit
        if digit != 6:
            result.append(str(digit))
            if len(result) == count:
                return "".join(result)
    raise AssertionError("digit search bound was insufficient")


def target_digits(precision: int) -> str:
    with localcontext() as context:
        context.prec = precision
        epsilon = Decimal(10) ** (-(precision - 10))
        pi = calculate_pi(epsilon)
        real, imaginary = dominant_pole(pi, epsilon)

        sine, cosine = sine_cosine(
            imaginary * LIMIT, pi, epsilon
        )
        norm_squared = real * real + imaginary * imaginary
        amplitude = 2 * (
            real * cosine + imaginary * sine
        ) / norm_squared

        logarithm = (
            real * LIMIT + abs(amplitude).ln()
        )
        logarithm_10 = Decimal(10).ln()
        decimal_order = logarithm / logarithm_10
        skipped_digits = int(
            (-decimal_order).to_integral_value(
                rounding=ROUND_FLOOR
            )
        ) - 5
        scaled_correction = (
            logarithm + skipped_digits * logarithm_10
        ).exp()
        if amplitude < 0:
            scaled_correction = -scaled_correction

        tail = Decimal(2) / 3 + scaled_correction
        return first_non_six_digits(tail)


def solve() -> str:
    with localcontext() as context:
        context.prec = 60
        alpha = Decimal(1).exp()
        assert first_non_six_digits(
            alpha * alpha - alpha - 4
        ) == "70774270"
        assert first_non_six_digits(
            alpha**3 - 2 * alpha**2 + alpha / 2 - 6
        ) == "55395558"

    lower_precision = target_digits(80)
    higher_precision = target_digits(110)
    assert lower_precision == higher_precision
    return higher_precision


if __name__ == "__main__":
    print(solve())
