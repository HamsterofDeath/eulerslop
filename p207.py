#!/usr/bin/env python3
# Project Euler 207: Integer Partition Equations
#
# Substitute x = 2^t. Then 4^t = 2^t + k becomes x^2 = x + k, so each
# partition corresponds to an integer x >= 2 with k = x(x-1). The partition
# is "perfect" exactly when t is an integer, i.e. when x is a power of 2.
#
# Counting partitions with k <= m where m = x(x-1):
#   total   = x - 1                     (x ranges over 2..x)
#   perfect = floor(log2(x))            (powers of 2 in 2..x)
#
# P only decreases between powers of 2, so find the smallest x with
# perfect/total < 1/12345 and return m = x(x-1).


def solve():
    target_num, target_den = 1, 12345
    perfect = 1  # x starts at 2, which is 2^1
    x = 2
    next_pow = 4
    while True:
        total = x - 1
        # perfect / total < 1/12345  <=>  perfect * 12345 < total
        if perfect * target_den < total * target_num:
            return x * (x - 1)
        # jump: within this block (until next power of 2), perfect is constant,
        # so the condition first holds at total = perfect*12345 + 1
        x_needed = perfect * target_den // target_num + 2
        x = min(x_needed, next_pow)
        if x == next_pow:
            perfect += 1
            next_pow *= 2


if __name__ == "__main__":
    print(solve())
