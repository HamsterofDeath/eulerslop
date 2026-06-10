#!/usr/bin/env python3
# Project Euler 284: Steady Squares in base 14.
#
# An n-digit steady square is x with x^2 = x (mod 14^n), i.e. an idempotent
# mod 14^n = 2^n * 7^n.  By CRT there are exactly four: 0, 1, and the two
# non-trivial idempotents a_n (= 0 mod 2^n, 1 mod 7^n) and b_n = 14^n + 1 - a_n.
# These are 14-adically stable: a_{n+1} = a_n (mod 14^n), so all of them are
# truncations of two fixed 14-adic digit streams starting 7, 8 (e.g. 7 -> 37
# -> c37 -> ...).
#
# We lift the idempotent e = 7 mod 14 to mod 14^10000 with the quadratically
# convergent Newton step for idempotents: e <- e^2 (3 - 2e), which doubles the
# precision each time.  Then for each n the n-digit steady squares are the two
# truncations whose leading digit (digit n-1) is non-zero (a zero leading
# digit means the truncation already occurred for a smaller n), plus the
# number 1 for n = 1.  Sum all their digit sums and print in base 14.

N = 10000
DIGITS = "0123456789abcd"


def to_base14(num):
    if num == 0:
        return "0"
    out = []
    while num:
        num, r = divmod(num, 14)
        out.append(DIGITS[r])
    return "".join(reversed(out))


def solve():
    # Hensel/Newton lifting of the idempotent congruent to 7 mod 14.
    e, prec = 7, 1
    while prec < N:
        prec = min(2 * prec, N)
        mod = 14 ** prec
        e = (e * e * (3 - 2 * e)) % mod

    big = 14 ** N
    a = e
    b = big + 1 - a  # the other non-trivial idempotent (starts with digit 8)

    total = 1  # the steady square "1" (n = 1)
    for x in (a, b):
        digits = []
        while x:
            x, r = divmod(x, 14)
            digits.append(r)
        digits += [0] * (N - len(digits))
        prefix = 0
        for n in range(1, N + 1):
            prefix += digits[n - 1]
            if digits[n - 1] != 0:  # valid n-digit number (no leading zero)
                total += prefix
    return to_base14(total)


if __name__ == "__main__":
    print(solve())
