#!/usr/bin/env python3

def crazy_sum(a, b, c):
    # For n <= b write k = floor((b - n) / a), so n lies in (b-(k+1)a, b-ka].
    # Unrolling the recursion F(n) = F(a+F(a+F(a+F(a+n)))): the innermost
    # argument a+n lies one band higher (k-1), and by induction every
    # intermediate value exceeds b (each is b plus positive multiples of a-c,
    # and a > c here), so each outer F just subtracts c after adding a.
    # Induction gives the closed form F(n) = n + 4(k+1)a - (3k+4)c.
    # (Check: a=50, b=2000, c=40 -> F(0) = 0 + 4*41*50 - 124*40 = 3240.)
    #
    # S = sum_{n=0}^{b} F(n) = sum n + 4a*sum(k+1) - c*sum(3k+4),
    # where sum_k = sum over n of floor((b-n)/a) has K = floor(b/a) full bands
    # of length a (values 0..K-1) plus a partial band of value K.
    K = b // a
    sum_k = a * K * (K - 1) // 2 + K * (b - K * a + 1)
    cnt = b + 1
    return b * (b + 1) // 2 + 4 * a * (sum_k + cnt) - c * (3 * sum_k + 4 * cnt)

def solve():
    assert crazy_sum(50, 2000, 40) == 5204240
    return crazy_sum(21 ** 7, 7 ** 21, 12 ** 7) % 10 ** 9

if __name__ == "__main__":
    print(solve())
