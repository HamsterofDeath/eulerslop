#!/usr/bin/env python3
"""Project Euler 768: balanced chandelier subsets."""

from collections import defaultdict


def prime_factors(n: int) -> list[int]:
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def radical(n: int) -> int:
    result = 1
    for p in prime_factors(n):
        result *= p
    return result


def mobius(n: int) -> int:
    count = 0
    d = 2
    while d * d <= n:
        if n % d == 0:
            n //= d
            count += 1
            if n % d == 0:
                return 0
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        count += 1
    return -1 if count % 2 else 1


def multiply(a: list[int], b: list[int]) -> list[int]:
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                result[i + j] += x * y
    return result


def divide_exact(a: list[int], b: list[int]) -> list[int]:
    a = a[:]
    quotient = [0] * (len(a) - len(b) + 1)
    for k in range(len(quotient) - 1, -1, -1):
        coeff = a[len(b) - 1 + k] // b[-1]
        quotient[k] = coeff
        for j, y in enumerate(b):
            a[j + k] -= coeff * y
    assert all(x == 0 for x in a[: len(b) - 1])
    return quotient


def cyclotomic(n: int) -> list[int]:
    numerator = [1]
    denominator = [1]
    for d in range(1, n + 1):
        if n % d == 0:
            poly = [-1] + [0] * (d - 1) + [1]
            mu = mobius(n // d)
            if mu == 1:
                numerator = multiply(numerator, poly)
            elif mu == -1:
                denominator = multiply(denominator, poly)
    return divide_exact(numerator, denominator)


def reduced_root_vectors(n: int) -> list[tuple[int, ...]]:
    phi = cyclotomic(n)
    degree = len(phi) - 1
    vectors = []
    for power in range(n):
        poly = [0] * (power + 1)
        poly[power] = 1
        while len(poly) > degree:
            coeff = poly[-1]
            if coeff:
                shift = len(poly) - degree - 1
                for i in range(degree):
                    poly[shift + i] -= coeff * phi[i]
            poly.pop()
        vectors.append(tuple(poly + [0] * (degree - len(poly))))
    return vectors


def subset_sums(vectors: list[tuple[int, ...]]) -> dict[tuple[int, tuple[int, ...]], int]:
    degree = len(vectors[0])
    result = defaultdict(int)
    for mask in range(1 << len(vectors)):
        total = [0] * degree
        for i, vector in enumerate(vectors):
            if mask >> i & 1:
                for j, value in enumerate(vector):
                    total[j] += value
        result[(mask.bit_count(), tuple(total))] += 1
    return result


def balanced_distribution(n: int) -> list[int]:
    vectors = reduced_root_vectors(n)
    middle = n // 2
    left = subset_sums(vectors[:middle])
    right = subset_sums(vectors[middle:])
    counts = [0] * (n + 1)
    for (left_size, left_sum), left_count in left.items():
        needed = tuple(-x for x in left_sum)
        for right_size in range(n - left_size + 1):
            counts[left_size + right_size] += (
                left_count * right.get((right_size, needed), 0)
            )
    return counts


def coefficient_power(poly: list[int], exponent: int, target: int) -> int:
    result = [1] + [0] * target
    base = poly[: target + 1]
    for _ in range(exponent):
        next_result = [0] * (target + 1)
        for i, x in enumerate(result):
            if x:
                for j, y in enumerate(base[: target + 1 - i]):
                    if y:
                        next_result[i + j] += x * y
        result = next_result
    return result[target]


def f(n: int, m: int) -> int:
    base = radical(n)
    classes = n // base
    return coefficient_power(balanced_distribution(base), classes, m)


def solve() -> int:
    assert f(4, 2) == 2
    assert f(12, 4) == 15
    assert f(36, 6) == 876
    return f(360, 20)


if __name__ == "__main__":
    print(solve())
