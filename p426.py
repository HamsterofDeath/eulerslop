# Project Euler 426: Box-Ball System
#
# The BBS is a soliton cellular automaton: the final state is the multiset of
# soliton sizes in ascending order. Solitons are found via the Takahashi-Satsuma
# decomposition: write balls as '(' and empty boxes as ')', match like nested
# parentheses; a matched pair's "pass number" is 1 + max pass of pairs nested
# directly inside it, and the number of solitons of size >= k equals the number
# of pairs with pass number k.
#
# On run lengths this becomes a linear stack algorithm: each ones-run pushes a
# group (count, v) where v is the max pass accumulated above its top element.
# A zeros-run of length b consumes groups: taking e = min(b, count) elements
# from group (c, v) creates pairs with passes v+1 .. v+e (its size-k solitons
# contribute sum of squares (v+e)^2 - v^2 since N_k covers k in [v+1, v+e]);
# a fully consumed group propagates v+c down to the group below (max). Trailing
# infinite empty boxes flush the stack the same way.
# Validated against direct simulation of the BBS dynamics on the statement's
# examples and hundreds of random configurations.

def solve():
    MOD = 50515093
    N = 10_000_001  # t_0 .. t_10_000_000, alternating occupied/empty runs

    s = 290797
    sc = []  # group counts (unmatched balls)
    sv = []  # group base pass values
    ans = 0
    occupied = True
    for _ in range(N):
        t = (s & 63) + 1
        s = s * s % MOD
        if occupied:
            sc.append(t)
            sv.append(0)
        else:
            b = t
            while b and sc:
                c = sc[-1]
                v = sv[-1]
                if b >= c:
                    sc.pop()
                    sv.pop()
                    b -= c
                    top = v + c
                    ans += top * top - v * v
                    if sv and sv[-1] < top:
                        sv[-1] = top
                else:
                    top = v + b
                    ans += top * top - v * v
                    sc[-1] = c - b
                    sv[-1] = top
                    b = 0
        occupied = not occupied

    # flush with the infinite empty boxes to the right
    while sc:
        c = sc.pop()
        v = sv.pop()
        top = v + c
        ans += top * top - v * v
        if sv and sv[-1] < top:
            sv[-1] = top

    return ans


if __name__ == "__main__":
    print(solve())
