#!/usr/bin/env python3
# Project Euler 281: Pizza Toppings
#
# A topping arrangement is a colouring of the m*n slices of a cycle with m
# colours, each used exactly n times, counted up to rotation only.
# By Burnside's lemma, a rotation k with g = gcd(k, mn) splits the cycle into
# g orbits of length mn/g; a fixed colouring gives every orbit one colour and
# needs g/m orbits per colour, so m | g.  Writing g = m*e (so e | n):
#
#   f(m, n) = (1/(mn)) * sum_{e | n} phi(n/e) * (m*e)! / (e!)^m
#
# (number of k with gcd(k,mn)=m*e is phi(mn/(m*e)) = phi(n/e)).
# f grows quickly in both m and n, so we just enumerate until f > 10^15.

from math import factorial, gcd

LIMIT = 10 ** 15


def phi(n):
    result, p, m = n, 2, n
    while p * p <= m:
        if m % p == 0:
            result -= result // p
            while m % p == 0:
                m //= p
        p += 1
    if m > 1:
        result -= result // m
    return result


def f(m, n):
    total = 0
    for e in range(1, n + 1):
        if n % e == 0:
            total += phi(n // e) * factorial(m * e) // factorial(e) ** m
    assert total % (m * n) == 0
    return total // (m * n)


def solve():
    answer = 0
    m = 2
    while True:
        # f(m,1) = (m-1)!; once even n=1 exceeds the limit, no larger m works.
        if f(m, 1) > LIMIT:
            break
        n = 1
        while True:
            v = f(m, n)
            if v > LIMIT:
                break
            answer += v
            n += 1
        m += 1
    return answer


if __name__ == "__main__":
    print(solve())
