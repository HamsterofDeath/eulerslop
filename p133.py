#!/usr/bin/env python3

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def order_mod(base, mod):
    phi = mod
    x = mod
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            phi -= phi // p
        p += 1 if p == 2 else 2
    if x > 1:
        phi -= phi // x

    order = phi
    temp = phi
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            while order % p == 0 and pow(base, order // p, mod) == 1:
                order //= p
            while temp % p == 0:
                temp //= p
        p += 1 if p == 2 else 2
    if temp > 1:
        if order % temp == 0 and pow(base, order // temp, mod) == 1:
            order //= temp
    return order

def can_divide_R10n(p):
    # Check if p divides R(10^n) for some n
    # This means order of 10 mod 9p has only prime factors 2 and 5
    if p == 2 or p == 5:
        return False
    ord_val = order_mod(10, 9 * p)
    while ord_val % 2 == 0:
        ord_val //= 2
    while ord_val % 5 == 0:
        ord_val //= 5
    return ord_val == 1

def solve():
    limit = 100_000
    total = 0
    for p in range(2, limit):
        if not is_prime(p):
            continue
        if p == 2 or p == 5:
            total += p
        elif not can_divide_R10n(p):
            total += p
    return total

if __name__ == "__main__":
    print(solve())
