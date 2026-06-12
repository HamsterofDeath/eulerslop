#!/usr/bin/env python3

from fractions import Fraction
from math import comb, factorial


MOD_BITS = 48
LOG_PRECISION = MOD_BITS + 20
MODULUS = 1 << MOD_BITS


def bernoulli_numbers(limit):
    work = [Fraction(0) for _ in range(limit + 1)]
    result = []
    for m in range(limit + 1):
        work[m] = Fraction(1, m + 1)
        for j in range(m, 0, -1):
            work[j - 1] = j * (work[j - 1] - work[j])
        result.append(work[0])
    return result


BERNOULLI = bernoulli_numbers(LOG_PRECISION)


def power_sum(n, exponent):
    if n <= 0:
        return 0
    total = Fraction(0)
    for k in range(exponent + 1):
        total += Fraction(comb(exponent + 1, k)) * BERNOULLI[k] * n ** (exponent + 1 - k)
    total /= exponent + 1
    return total.numerator


def v2(value):
    if value == 0:
        return 10**9
    value = abs(value)
    return (value & -value).bit_length() - 1


def divide_mod_power_of_two(numerator, denominator, bits):
    twos = v2(denominator)
    odd = denominator >> twos
    assert numerator % (1 << twos) == 0
    return ((numerator >> twos) % (1 << bits)) * pow(odd, -1, 1 << bits) % (1 << bits)


def exp_2_adic(log_value, bits):
    result = 1 % (1 << bits)
    for j in range(1, bits + 1):
        denominator = factorial(j)
        if v2(log_value) * j - v2(denominator) >= bits:
            continue
        needed_bits = bits + v2(denominator)
        numerator = pow(log_value, j, 1 << needed_bits)
        result = (result + divide_mod_power_of_two(numerator, denominator, bits)) % (1 << bits)
    return result


def odd_product_upto(limit, bits=MOD_BITS):
    """Product of all odd positive integers not exceeding limit, modulo 2**bits."""
    odd_count = (limit + 1) // 2
    pair_count = odd_count // 2
    has_leftover = odd_count & 1

    log_bits = bits + 20
    log_modulus = 1 << log_bits
    log_value = 0

    for power in range(1, log_bits + 1):
        if 2 * power - v2(power) >= log_bits:
            continue

        term_base = (
            (1 if power & 1 else -1) * power_sum(pair_count - 1, power)
            - power_sum(pair_count, power)
        )
        if has_leftover:
            term_base += (1 if power & 1 else -1) * pair_count**power
        if term_base == 0:
            continue

        numerator = 4**power * term_base
        term = divide_mod_power_of_two(abs(numerator), power, log_bits)
        if numerator < 0:
            term = -term
        log_value = (log_value + term) % log_modulus

    result = exp_2_adic(log_value, bits)
    if pair_count & 1:
        result = (-result) % (1 << bits)
    return result


def odd_factorial_part(n, bits=MOD_BITS):
    result = 1
    modulus = 1 << bits
    while n:
        result = result * odd_product_upto(n, bits) % modulus
        n //= 2
    return result


def last_hex_digits_before_zeroes(n):
    twos = n - n.bit_count()
    value = odd_factorial_part(n) * (1 << (twos % 4)) % MODULUS
    return f"{value:012X}"


def solve():
    assert last_hex_digits_before_zeroes(20) == "21C3677C82B4"
    return last_hex_digits_before_zeroes(factorial(20))


if __name__ == "__main__":
    print(solve())
