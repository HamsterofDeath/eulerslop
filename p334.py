#!/usr/bin/env python3

def sum_squares(a, b):
    # sum of t^2 for t = a..b (works for negative bounds too)
    def f(n):
        return n * (n + 1) * (2 * n + 1) // 6
    return f(b) - f(a - 1)

def solve():
    # Generate the bean counts b_1..b_1500 from the t-sequence.
    t = 123456
    beans = []
    for _ in range(1500):
        t = t // 2 if t % 2 == 0 else (t // 2) ^ 926252
        beans.append((t % 2048) + 1)
    assert beans[0] == 289 and beans[1] == 145

    def moves(bs):
        # A move at bowl k sends one bean to k-1 and one to k+1.  This keeps
        # B = total beans and S = sum of bean positions invariant, while
        # Q = sum of squared positions increases by exactly 2 per move:
        # (k-1)^2 + (k+1)^2 - 2k^2 = 2.  Hence #moves = (Q_final - Q_initial)/2.
        B = sum(bs)
        S = sum(i * b for i, b in enumerate(bs))
        Q = sum(i * i * b for i, b in enumerate(bs))
        # The process is confluent: the final 0/1 state is unique and is an
        # interval of occupied bowls, possibly with a single internal hole,
        # determined by the invariants B and S.
        num = S - B * (B - 1) // 2
        if num % B == 0:
            # Full interval a..a+B-1.
            a = num // B
            Qf = sum_squares(a, a + B - 1)
        else:
            # Interval a..a+B with one hole h strictly inside.
            # Sum condition: (B+1)a + B(B+1)/2 - h = S with a < h < a+B,
            # which pins a to the unique multiple-of-B window.
            lo = S - B * (B + 1) // 2 + 1
            a = -(-lo // B)  # ceil(lo / B)
            h = (B + 1) * a + B * (B + 1) // 2 - S
            assert a < h < a + B
            Qf = sum_squares(a, a + B) - h * h
        return (Qf - Q) // 2

    assert moves(beans[:2]) == 3419100  # given example b1=289, b2=145
    return moves(beans)

if __name__ == "__main__":
    print(solve())
