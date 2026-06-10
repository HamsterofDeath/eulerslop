#!/usr/bin/env python3
from math import factorial

# Number caterpillar: pieces 1..40 placed in random order; segments = maximal
# runs of placed pieces.  M = maximum segment count during the process.
#
# Counting permutations by the *event type* sequence (New segment / Grow a
# segment / Merge two segments) turns out to be position-independent: the
# number of permutations whose history goes  j -> j' segments at each step is
# obtained with multiplicative weights
#     New   (j -> j+1): weight j+1
#     Grow  (j -> j  ): weight 2j
#     Merge (j -> j-1): weight j-1
# (a classical bijection: building the permutation by runs; verified against
# the n=10 table given in the problem).  So a tiny DP over
# (pieces placed, current segments, max segments so far) with exact integers
# gives the full distribution of M.

def distribution(n):
    # dp[(j, mx)] = number of placement orders of i pieces with j segments now
    # and maximum mx so far.
    dp = {(0, 0): 1}
    for _ in range(n):
        ndp = {}
        for (j, mx), w in dp.items():
            # new segment
            key = (j + 1, max(mx, j + 1))
            ndp[key] = ndp.get(key, 0) + w * (j + 1)
            if j >= 1:
                # grow an existing segment (left or right end)
                key = (j, mx)
                ndp[key] = ndp.get(key, 0) + w * (2 * j)
            if j >= 2:
                # merge two adjacent segments
                key = (j - 1, mx)
                ndp[key] = ndp.get(key, 0) + w * (j - 1)
        dp = ndp
    # all pieces placed -> exactly one segment
    counts = {}
    for (j, mx), w in dp.items():
        if j == 1:
            counts[mx] = counts.get(mx, 0) + w
    return counts

def solve():
    n = 40
    counts = distribution(n)
    total = factorial(n)
    assert sum(counts.values()) == total
    num = sum(mx * w for mx, w in counts.items())  # E[M] = num / 40!
    # round num/total to 6 decimal places (half-up; exact integer arithmetic)
    scaled = (num * 10 ** 6 * 2 + total) // (2 * total)
    return f"{scaled // 10 ** 6}.{scaled % 10 ** 6:06d}"

if __name__ == "__main__":
    print(solve())
