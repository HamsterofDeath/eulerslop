#!/usr/bin/env python3

def g_of(digits, pow10):
    # Expected position where a pattern of d digits first ends in a random
    # decimal stream is sum of 10^b over all borders b of the pattern
    # (lengths b where prefix == suffix, including b = d).  This is the
    # classical correlation-polynomial result for waiting times.
    # g(n) is the expected *start* index, so subtract d - 1.
    d = len(digits)
    # KMP failure function: fail[k] = length of longest proper border of
    # the prefix of length k.
    fail = [0] * (d + 1)
    k = 0
    for q in range(1, d):
        c = digits[q]
        while k > 0 and digits[k] != c:
            k = fail[k]
        if digits[k] == c:
            k += 1
        fail[q + 1] = k
    total = 0
    t = d
    while t > 0:
        total += pow10[t]
        t = fail[t]
    return total - d + 1

def solve():
    N = 10 ** 16
    pow10 = [10 ** i for i in range(20)]
    total = 0
    for n in range(2, 1000000):
        total += g_of(str(N // n), pow10)
    return total

if __name__ == "__main__":
    print(solve())
