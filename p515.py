#!/usr/bin/env python3


def _is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 3, 5, 7):
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def D(a, b, k):
    # Repeated prefix sums give
    # d(p,p-1,k) = sum_i C(p-1-i+k-1,k-1)/i.
    # Modulo p and for k < p this reduces to (k-1)^(-1).
    return sum(pow(k - 1, -1, p) for p in range(a, a + b) if _is_prime(p))


def solve():
    assert D(101, 1, 10) == 45
    assert D(10 ** 3, 10 ** 2, 10 ** 2) == 8334
    assert D(10 ** 6, 10 ** 3, 10 ** 3) == 38162302
    return D(10 ** 9, 10 ** 5, 10 ** 5)


if __name__ == "__main__":
    print(solve())
