#!/usr/bin/env python3

def solve():
    # A weak Goodstein step (bump base b -> b+1, subtract 1) acts on the digit
    # string of g: reinterpreting never changes digits, so only the subtraction
    # does.  Clearing a nonzero low digit d takes exactly d steps (base += d).
    # A digit c at position k with zeros below is cleared by c "cycles"; one
    # cycle is: borrow (1 step, lower positions become the old base b), then
    # clear positions 0..k-1 bottom-up.  This yields closed forms for the final
    # base psi(b, c, k) starting from digit c at position k, zeros below:
    #   psi(b, c, 0) = b + c
    #   psi(b, c, 1) = (b+1)*2^c - 1
    #   psi(b, c, 2) = E^c(b)   where E(y) = (2y+2)*2^y - 1
    #   psi(b, 1, 3) = E^(b+1)(b)
    # Digits of n < 16 are processed LSB-first; G(n) = final base - 2.
    # E iterates produce towers of exponents, so huge values are stored as
    # residue vectors along the totient chain m0 = 10^9, m_{i+1} = phi(m_i),
    # using the generalized Euler theorem 2^y = 2^(y mod phi(m) + phi(m))
    # (mod m), valid whenever y >= log2(m).

    MOD = 10 ** 9

    def phi(n):
        r, x, p = n, n, 2
        while p * p <= x:
            if x % p == 0:
                while x % p == 0:
                    x //= p
                r -= r // p
            p += 1
        if x > 1:
            r -= r // x
        return r

    ms = [MOD]
    while ms[-1] > 1:
        ms.append(phi(ms[-1]))
    L = len(ms)

    EXACT_LIMIT = 10 ** 5  # keep exact ints while the exponent stays this small

    def to_vec(v):
        return [v % m for m in ms]

    def E_step(y):
        # one application of E(y) = (2y+2)*2^y - 1
        if isinstance(y, int):
            if y <= EXACT_LIMIT:
                return (2 * y + 2) * (1 << y) - 1
            y = to_vec(y)  # y > 10^5 >= log2(m_i) for every level: Euler valid
        out = []
        for i in range(L):
            m = ms[i]
            if m == 1:
                out.append(0)
                continue
            e = y[i + 1] + ms[i + 1]  # y mod phi(m) + phi(m)
            out.append(((2 * y[i] + 2) * pow(2, e, m) - 1) % m)
        return out

    def G(n):
        # process binary digits of n, LSB first; base starts at 2
        base = 2
        pos = 0
        while n:
            if n & 1:
                if pos == 0:
                    base += 1
                elif pos == 1:
                    base = 2 * base + 1
                elif pos == 2:
                    base = E_step(base)
                else:  # pos == 3, base is still a small int here (<= 2047)
                    for _ in range(base + 1):
                        base = E_step(base)
            n >>= 1
            pos += 1
        # G(n) = final base - 2
        if isinstance(base, int):
            return base - 2
        return (base[0] - 2) % MOD

    # sanity checks from the problem statement (all stay exact)
    assert G(2) == 3 and G(4) == 21 and G(6) == 381
    assert sum(G(k) for k in range(1, 8)) == 2517

    return sum(G(k) for k in range(1, 16)) % MOD


if __name__ == "__main__":
    print(solve())
