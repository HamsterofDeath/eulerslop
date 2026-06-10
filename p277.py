#!/usr/bin/env python3

def solve():
    # Each step of the modified Collatz map is affine with multiplier in
    # {1/3, 4/3, 2/3}; a_i = (c_i * a_1 + d_i) / 3^(i-1) with gcd(c_i, 3) = 1.
    # Hence the i-th step letter depends only on a_1 mod 3^i, and the full
    # 30-letter prefix is determined by a_1 mod 3^30. The valid starting
    # values form exactly one residue class mod 3^30 (each base-3 digit lift
    # hits the three letters once because c_i is invertible mod 3).
    target = "UDDDUdddDDUDDddDdDddDDUDDdUUDd"
    L = len(target)
    M = 3 ** L

    def prefix(a, k):
        # First k step letters of the sequence starting at a (a >= 3^L, so it
        # cannot terminate within L steps: each step keeps a_n >= a / 3^n).
        out = []
        for _ in range(k):
            r = a % 3
            if r == 0:
                a //= 3
                out.append("D")
            elif r == 1:
                a = (4 * a + 2) // 3
                out.append("U")
            else:
                a = (2 * a - 1) // 3
                out.append("d")
        return "".join(out)

    # Lift the residue one base-3 digit at a time.
    res = 0
    pw = 1
    for k in range(1, L + 1):
        for t in range(3):
            cand = res + t * pw
            # Add M so the trial value is large enough to run k steps;
            # this does not change cand mod 3^k.
            if prefix(cand + M, k) == target[:k]:
                res = cand
                break
        pw *= 3

    # Smallest member of the residue class strictly above 10^15.
    lo = 10 ** 15
    return res + ((lo - res) // M + 1) * M

if __name__ == "__main__":
    print(solve())
