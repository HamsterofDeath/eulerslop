#!/usr/bin/env python3
import math
import numpy as np

def solve():
    # p = product of the 42 primes below 190.  PSR(p) is the largest divisor
    # d of p with d^2 <= p, i.e. the subset of primes whose product is the
    # largest one not exceeding sqrt(p).  Meet in the middle: split the primes
    # into two halves of 21 (interleaved so the halves balance), enumerate the
    # 2^21 subset log-sums of each half, sort one side, and for every subset
    # of the other side binary-search the best partner.  Floating point only
    # ranks candidates; near-optimal pairs (within a safety window) are
    # re-verified with exact big-integer arithmetic.
    primes = [p for p in range(2, 190)
              if all(p % q for q in range(2, int(p ** 0.5) + 1))]
    A, B = primes[0::2], primes[1::2]

    def subset_logs(half):
        # logs[i] = sum of log(half[k]) over set bits k of i
        logs = np.zeros(1)
        for p in half:
            logs = np.concatenate([logs, logs + math.log(p)])
        return logs

    def subset_product(half, idx):
        prod = 1
        for k, p in enumerate(half):
            if (idx >> k) & 1:
                prod *= p
        return prod

    la = subset_logs(A)
    lb = subset_logs(B)
    order = np.argsort(lb)
    lbs = lb[order]
    target = (la[-1] + lb[-1]) / 2.0  # log(sqrt(p))

    EPS_HI = 1e-9   # float slack above the target
    EPS_LO = 1e-7   # candidate window below the best approximate sum

    # For each A-subset, B-partners with log <= target - la (+ slack).
    hi = np.searchsorted(lbs, target - la + EPS_HI, side="right")
    valid = hi > 0
    combined = np.where(valid, la + lbs[np.maximum(hi - 1, 0)], -np.inf)
    best_approx = combined.max()
    lo = np.searchsorted(lbs, best_approx - EPS_LO - la, side="left")

    P = 1
    for p in primes:
        P *= p

    best = 0
    for i in np.nonzero(lo < hi)[0]:
        pa = subset_product(A, int(i))
        for j in range(int(lo[i]), int(hi[i])):
            v = pa * subset_product(B, int(order[j]))
            if v > best and v * v <= P:
                best = v
    return best % 10 ** 16

if __name__ == "__main__":
    print(solve())
