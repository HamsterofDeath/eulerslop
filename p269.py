#!/usr/bin/env python3
from collections import defaultdict

def solve():
    # P_n has non-negative digit coefficients with positive leading digit, so
    # it is positive for x > 0; x = 0 is a root iff the last digit is 0, and
    # a root x = -r needs a_d * r^d <= 9(r^d-1)/(r-1), forcing r <= 9.
    # So an integer root lies in {0, -1, ..., -9}.
    #
    # Leading zeros do not change polynomial values, so Z(10^16) equals the
    # number of 16-digit strings (leading zeros allowed, i.e. n in
    # [0, 10^16)) whose polynomial has a root in that set: the all-zero
    # string (n = 0, excluded) is exactly compensated by n = 10^16 = 1e16
    # (polynomial x^16, root 0, included).
    #
    # Digit DP, most significant digit first.  State: for each r in 1..9 the
    # Horner value v -> -r*v + digit, or DEAD once |v| provably cannot return
    # to 0 with the remaining digits (the j remaining digits can change the
    # final value by at most 9(r^j-1)/(r-1), so |v| > 9(r^j-1)/((r-1) r^j)
    # is hopeless; for r = 1 the bound is 9*ceil(j/2)).  DEAD components are
    # capped, which keeps the joint state space tiny.
    L = 16
    DEAD = None
    RS = range(1, 10)

    # bound[r][j]: max |v| that can still reach 0 with j digits left
    bound = [[0] * (L + 1) for _ in range(10)]
    for j in range(L + 1):
        bound[1][j] = 9 * ((j + 1) // 2)
        for r in range(2, 10):
            bound[r][j] = (9 * (r ** j - 1)) // ((r - 1) * r ** j)

    states = {(0,) * 9: 1}
    for pos in range(L - 1):  # first 15 digits; the last digit is special
        j = L - 1 - pos       # digits remaining after this one
        bnd = [None] + [bound[r][j] for r in RS]
        new = defaultdict(int)
        for st, c in states.items():
            for d in range(10):
                ns = []
                for r in RS:
                    v = st[r - 1]
                    if v is DEAD:
                        ns.append(DEAD)
                        continue
                    nv = d - r * v
                    ns.append(nv if -bnd[r] <= nv <= bnd[r] else DEAD)
                new[tuple(ns)] += c
        states = new

    # Last digit d: success iff d = 0 (root x=0) or some alive component
    # satisfies -r*v + d = 0, i.e. d = r*v with 0 <= d <= 9.
    total = 0
    for st, c in states.items():
        finishing = {0}  # d = 0 always succeeds via the root x = 0
        for r in RS:
            v = st[r - 1]
            if v is not DEAD and 0 <= r * v <= 9:
                finishing.add(r * v)
        total += c * len(finishing)
    return total

if __name__ == "__main__":
    print(solve())
