#!/usr/bin/env python3
from bisect import bisect_left, bisect_right

# S = "123456789101112..." (1-indexed positions).
# f(n) = start position of the n-th occurrence of str(n) in S.
#
# Strategy: let C(N) = number of occurrences of the pattern whose starting
# character lies inside the digits of some number m <= N.  Occurrences ordered
# by start position are ordered by (m, offset), so C is what we need to rank
# them.  For numbers m <= BASE we count by direct string search; for larger m
# (>= 8 digits > pattern length <= 7) an occurrence touches at most two
# consecutive numbers, so it is either interior to m or split between a suffix
# of m and a prefix of m+1 -- both countable by digit arithmetic.  Binary
# search on N then locates the number containing the n-th occurrence.

BASE = 10 ** 6  # occurrences starting in numbers 1..BASE handled by brute force

def cumlen(n):
    """Total number of digits of 1,2,...,n."""
    if n <= 0:
        return 0
    k = len(str(n))
    total = sum(9 * 10 ** (d - 1) * d for d in range(1, k))
    return total + (n - 10 ** (k - 1) + 1) * k

def count_at_offset_upto(x, k, i, sval, d):
    """Count k-digit m <= x whose digits i..i+d-1 (0-based from the left)
    spell the d-digit value sval (sval has no leading zero)."""
    if x < 10 ** (k - 1):
        return 0
    x = min(x, 10 ** k - 1)
    right = 10 ** (k - i - d)        # free digits to the right of the pattern
    pmin = 10 ** (i - 1) if i > 0 else 0  # smallest valid prefix value
    hip = x // (right * 10 ** d)     # prefix (first i digits) of x
    cnt = (hip - pmin) * right if hip > pmin else 0
    mid = (x // right) % 10 ** d     # digits i..i+d-1 of x
    if mid > sval:
        cnt += right
    elif mid == sval:
        cnt += x % right + 1
    return cnt

def count_interior(lo, hi, k, s):
    """Occurrences of s fully inside one k-digit number m, lo <= m <= hi."""
    d = len(s)
    sval = int(s)
    cnt = 0
    for i in range(0, k - d + 1):
        cnt += (count_at_offset_upto(hi, k, i, sval, d)
                - count_at_offset_upto(lo - 1, k, i, sval, d))
    return cnt

def count_ap(a, b, m, r):
    """Count integers x in [a, b] with x % m == r."""
    if a > b:
        return 0
    return (b - r) // m - (a - 1 - r) // m

def count_boundary(lo, hi, k, s):
    """Occurrences of s starting inside a k-digit number m (lo <= m <= hi)
    and spilling over into m+1: last t digits of m are s[:t], and m+1 starts
    with s[t:]."""
    d = len(s)
    cnt = 0
    for t in range(1, d):
        if s[t] == '0':
            continue  # a number cannot start with digit 0
        s1 = int(s[:t])           # required value of m mod 10^t
        a_pref = int(s[t:])       # required prefix of m+1, d-t digits
        j = k - (d - t)           # free digits of m+1 after the prefix
        # x = m+1 is k-digit (the 10^k-1 rollover is handled below)
        a = max(a_pref * 10 ** j, lo + 1)
        b = min((a_pref + 1) * 10 ** j - 1, hi + 1, 10 ** k - 1)
        cnt += count_ap(a, b, 10 ** t, (s1 + 1) % 10 ** t)
    # special case m = 10^k - 1, where m+1 has k+1 digits
    m = 10 ** k - 1
    if lo <= m <= hi:
        local = str(m) + str(m + 1)
        for i in range(max(1, k - d + 1), k):
            if local[i:i + d] == s:
                cnt += 1
    return cnt

def make_counter(s, brute_positions):
    """Return C(N): occurrences of s starting inside numbers <= N (N >= BASE)."""
    nb = len(brute_positions)

    def C(N):
        cnt = nb
        kmax = len(str(N))
        for k in range(len(str(BASE + 1)), kmax + 1):
            lo = max(BASE + 1, 10 ** (k - 1))
            hi = min(N, 10 ** k - 1)
            if lo > hi:
                continue
            cnt += count_interior(lo, hi, k, s)
            cnt += count_boundary(lo, hi, k, s)
        return cnt

    return C

def occ_positions(text, s, limit):
    """All start positions (1-indexed) <= limit of s in text (overlapping)."""
    res = []
    p = text.find(s)
    while p != -1 and p < limit:
        res.append(p + 1)
        p = text.find(s, p + 1)
    return res

def f(n, prefix_str, prefix_chars):
    s = str(n)
    brute = occ_positions(prefix_str, s, prefix_chars)
    if n <= len(brute):
        return brute[n - 1]
    C = make_counter(s, brute)
    lo, hi = BASE, 2 * BASE
    while C(hi) < n:
        hi *= 2
    # smallest N with C(N) >= n: the n-th occurrence starts inside number N
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if C(mid) >= n:
            hi = mid
        else:
            lo = mid
    N = hi
    before = C(N - 1)
    local = str(N) + str(N + 1)
    offs = [i for i in range(len(str(N)))
            if local[i:i + len(s)] == s]
    return cumlen(N - 1) + offs[n - before - 1] + 1

def solve():
    # brute-force prefix: numbers 1..BASE+2 (the +2 lets occurrences that
    # start inside number BASE run past its end)
    prefix_str = ''.join(map(str, range(1, BASE + 3)))
    prefix_chars = cumlen(BASE)  # only count starts inside numbers <= BASE
    return sum(f(3 ** k, prefix_str, prefix_chars) for k in range(1, 14))

if __name__ == "__main__":
    print(solve())
