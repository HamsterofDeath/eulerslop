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

def solve():
    target = 40
    k = 10**9  # R(k) where k = 10^9
    primes = []
    # p=3: R(k) divisible by 3 iff k mod 3 == 0. 10^9 mod 3 = 1, so not included.
    p = 7  # skip 2,3,5
    while len(primes) < target:
        if is_prime(p):
            if p == 3:
                if k % 3 == 0:
                    primes.append(3)
            else:
                order = order_mod(10, p)  # for p>3, ord_p(10)
                if k % order == 0:
                    primes.append(p)
        p += 2
    return sum(primes)

if __name__ == "__main__":
    print(solve())
