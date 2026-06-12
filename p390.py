#!/usr/bin/env python3

def solve():
    # A triangle with sides sqrt(1+b^2), sqrt(1+c^2), sqrt(b^2+c^2) is the one
    # cut from the corner of a box with vertices (1,0,0), (0,b,0), (0,0,c); its
    # area is sqrt(b^2 + c^2 + b^2 c^2) / 2.  So with m = 2*Area we need
    #     m^2 = b^2 + c^2 + b^2 c^2,  i.e.  (b^2+1)(c^2+1) = m^2 + 1.
    # Mod 4 this forces b and c both even (then m is even and Area integral).
    #
    # For fixed b it is the Pell-type equation m^2 - (b^2+1) c^2 = b^2 whose
    # automorphism is (u, v) = (2b^2+1, 2b), since u^2 - (b^2+1) v^2 = 1.
    # Every solution descends (c -> u*c - 2b*m) to a fundamental one with
    # |c| < b, which is itself a solution with the roles swapped.  Hence all
    # solutions form a forest rooted at the degenerate pairs (a, b) = (0, b):
    # from a solution a < b with double-area m we get exactly the children
    #   (b, u*a + 2b*m)   ascending in the class of (m,  a),  u = 2b^2+1
    #   (b, 2b*m - u*a)   ascending in the conjugate class (m, -a), a > 0
    #   (a, u'*b + 2a*m)  continuing the chain with parameter a,  u' = 2a^2+1
    # m strictly increases along every edge, so DFS bounded by m <= 2n visits
    # each triangle {b, c} exactly once.  (Verified against brute force.)
    n = 10 ** 10
    mlim = 2 * n
    total = 0

    stack = []
    b = 2
    while (2 * b * b + 1) * b <= mlim:  # root (0, b) -> first child (b, 2b^2)
        stack.append((b, 2 * b * b, (2 * b * b + 1) * b))
        b += 2

    while stack:
        a, b, m = stack.pop()
        total += m // 2  # area of this triangle
        u, dv = 2 * b * b + 1, 2 * b * (b * b + 1)
        m1 = u * m + dv * a
        if m1 <= mlim:
            stack.append((b, u * a + 2 * b * m, m1))
        if a:
            m2 = u * m - dv * a
            if m2 <= mlim:
                stack.append((b, 2 * b * m - u * a, m2))
            ua, dva = 2 * a * a + 1, 2 * a * (a * a + 1)
            m3 = ua * m + dva * b
            if m3 <= mlim:
                stack.append((a, ua * b + 2 * a * m, m3))
    return total

if __name__ == "__main__":
    print(solve())
