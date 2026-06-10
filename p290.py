#!/usr/bin/env python3
"""Project Euler 290: Digital signature.

Count 0 <= n < 10^18 with digitsum(n) == digitsum(137*n).

Digit DP over the 18 decimal digits of n, least significant first.  While
multiplying by 137 digit by digit, the state is
  (carry, diff)  with  diff = digitsum(n so far) - digitsum(137n so far).
Appending digit a: t = 137*a + carry produces product digit t % 10 and new
carry t // 10 (carry stays < 137).  After all 18 digits the remaining
product digits are exactly the decimal digits of the final carry, so n
qualifies iff diff == digitsum(carry).
"""

from collections import defaultdict


def solve():
    DIGITS = 18
    dp = {(0, 0): 1}  # (carry, diff) -> count
    for _ in range(DIGITS):
        ndp = defaultdict(int)
        for (c, d), cnt in dp.items():
            for a in range(10):
                t = 137 * a + c
                ndp[(t // 10, d + a - t % 10)] += cnt
        dp = ndp

    total = 0
    for (c, d), cnt in dp.items():
        if d == sum(map(int, str(c))):
            total += cnt
    return total


if __name__ == "__main__":
    print(solve())
