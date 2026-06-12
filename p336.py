#!/usr/bin/env python3

def solve():
    # Each turntable use reverses a suffix of the train.  Simon places carriage
    # 1, then 2, ...: a carriage already in place costs 0 rotations, one at the
    # rear costs 1 (reverse the remaining suffix), anything else costs 2
    # (reverse to bring it to the rear, then reverse the suffix).  The maximum
    # is therefore 2(n-2)+1 = 2n-3 rotations: carriages 1..n-2 each cost 2 and
    # carriage n-1 costs 1; such worst cases are the maximix arrangements.
    #
    # Run Simon's first (double) move backwards: if P is maximix for n, then
    # after the two reversals position 1 holds carriage 1 and positions 2..n
    # hold a maximix arrangement of n-1 carriages.  Conversely, every maximix
    # arrangement of n arises from a maximix arrangement R of n-1 by forming
    # Q = (1, R+1), reversing the whole train, then reversing the suffix
    # starting at j for any j in 2..n-1 (this leaves carriage 1 at position j,
    # neither in place nor at the rear, so both moves really are forced).
    # Hence there are (n-2)! maximix arrangements; generate them all for n=11
    # (9! = 362880), sort, and take the 2011th.
    n_target = 11
    arrs = [(2, 1)]  # the unique maximix arrangement for 2 carriages
    for n in range(3, n_target + 1):
        new = []
        for r in arrs:
            q = (1,) + tuple(v + 1 for v in r)
            t = q[::-1]
            for j in range(2, n):  # 1-indexed split position
                new.append(t[:j - 1] + t[j - 1:][::-1])
        arrs = new
    arrs.sort()
    return ''.join(chr(ord('A') + v - 1) for v in arrs[2010])

if __name__ == "__main__":
    print(solve())
