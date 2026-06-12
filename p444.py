"""Project Euler 444: The Roundtable Lottery.

Exact game analysis (verified below by full optimal-play recursion for small p):
the revealed-ticket sequence is a uniform random permutation regardless of play,
and under optimal strategy E(p) = H_p (the p-th harmonic number).

Iterated sums telescope to the closed form (verified exactly for small k, N):
    S_k(N) = C(N+k, k) * (H_{N+k} - H_k)
so S_20(10^14) only needs C(N+20, 20) exactly and H_{N+20} via the asymptotic
expansion H_m = ln m + gamma + 1/(2m) - 1/(12m^2) + 1/(120m^4) - ...
"""
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction
from functools import lru_cache
from math import comb

# Euler-Mascheroni constant to 70 digits (mathematical constant)
GAMMA = Decimal("0.5772156649015328606065120900824024310421593359399235988057672348848677")


def E_exact(p):
    """Expected players remaining for p players, by optimal-play backward induction.

    State: U = unrevealed ticket values (players yet to act), A = revealed values
    still held at the table. Each turn reveals the acting player's ticket: either
    they scratch it (stay seated), or they take max(A) and leave, forcing the
    robbed max-holder to scratch the trader's ticket.
    """

    @lru_cache(maxsize=None)
    def g(U, A, x):
        # expected final value of a seated player currently holding revealed x
        if not U:
            return Fraction(x)
        if decide(U, A):
            M = max(A)
            return sum(g(U - {y}, (A - {M}) | {y}, y if x == M else x)
                       for y in U) / len(U)
        return sum(g(U - {y}, A | {y}, x) for y in U) / len(U)

    @lru_cache(maxsize=None)
    def decide(U, A):
        # acting player trades iff max(A) beats the EV of scratching own ticket
        if not A:
            return False
        scratch_ev = sum(g(U - {y}, A | {y}, y) for y in U) / len(U)
        return max(A) > scratch_ev

    @lru_cache(maxsize=None)
    def remaining(U, A):
        # expected number of scratch-decisions (= players left at the end)
        if not U:
            return Fraction(0)
        if decide(U, A):
            M = max(A)
            return sum(remaining(U - {y}, (A - {M}) | {y}) for y in U) / len(U)
        return 1 + sum(remaining(U - {y}, A | {y}) for y in U) / len(U)

    return remaining(frozenset(range(1, p + 1)), frozenset())


def H_frac(n):
    return sum(Fraction(1, i) for i in range(1, n + 1))


def fmt_sci(d, sig=10):
    """Scientific notation, sig significant digits, lowercase e, bare exponent."""
    e = d.adjusted()
    mant = d.scaleb(-e).quantize(Decimal(1).scaleb(-(sig - 1)), rounding=ROUND_HALF_UP)
    if mant >= 10:  # rounding carried over
        mant = (mant / 10).quantize(Decimal(1).scaleb(-(sig - 1)))
        e += 1
    return f"{mant}e{e}"


def solve():
    getcontext().prec = 80

    # 1) Verify E(p) = H_p exactly via the full game recursion for small p
    for p in range(1, 8):
        assert E_exact(p) == H_frac(p), f"E({p}) != H_{p}"

    # 2) Verify the closed form S_k(N) = C(N+k,k)(H_{N+k}-H_k) by brute iteration
    cur = [H_frac(p) for p in range(1, 21)]
    for k in range(1, 5):
        acc = Fraction(0)
        cur = [(acc := acc + v) for v in cur]
        assert all(cur[N - 1] == comb(N + k, k) * (H_frac(N + k) - H_frac(k))
                   for N in range(1, 21)), f"closed form fails at k={k}"

    # 3) Verify the statement's example S_3(100) = 5.983679014e5
    ex = comb(103, 3) * (H_frac(103) - H_frac(3))
    assert fmt_sci(Decimal(ex.numerator) / Decimal(ex.denominator)) == "5.983679014e5"

    # 4) S_20(10^14) = C(N+20,20) * (H_{N+20} - H_20)
    N, k = 10 ** 14, 20
    m = N + k
    dm = Decimal(m)
    h_m = dm.ln() + GAMMA + 1 / (2 * dm) - 1 / (12 * dm ** 2) + 1 / (120 * dm ** 4)
    h_k = H_frac(k)
    h_k_dec = Decimal(h_k.numerator) / Decimal(h_k.denominator)
    ans = Decimal(comb(m, k)) * (h_m - h_k_dec)
    return fmt_sci(ans)


if __name__ == "__main__":
    print(solve())
