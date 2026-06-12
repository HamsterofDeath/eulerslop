import numpy as np


def solve(N=10**7):
    # a^2 = a (mod n) iff n | a(a-1); since gcd(a, a-1) = 1, by CRT the
    # idempotents mod n are exactly the CRT combinations choosing a = 0 or
    # a = 1 modulo each prime-power component of n. There are 2^omega(n) of
    # them; M(n) is the largest. Build idempotent sets level by level over
    # omega(n) with numpy: every n with omega(n)=k lifts the 2^(k-1)
    # idempotents of rest = n / q (q = component of the smallest prime).
    idx = np.arange(N + 1, dtype=np.int64)

    # Smallest-prime-factor sieve.
    spf = np.zeros(N + 1, dtype=np.int32)
    for i in range(2, int(N**0.5) + 1):
        if spf[i] == 0:
            sl = spf[i * i :: i]
            sl[sl == 0] = i
    unset = spf == 0
    spf[unset] = idx[unset].astype(np.int32)  # remaining n >= 2 are prime
    spf64 = spf.astype(np.int64)

    # q[n] = p^v with p = spf[n], v = full multiplicity of p in n.
    q = spf64.copy()
    q[0] = q[1] = 1
    active = idx[2:]
    while active.size:
        r = active // q[active]
        more = r % spf64[active] == 0
        active = active[more]
        q[active] *= spf64[active]
    rest = idx // np.maximum(q, 1)  # n with its smallest-prime component removed

    # omega[n] = number of distinct primes, via the rest-chain (<= 8 rounds).
    omega = np.zeros(N + 1, dtype=np.int8)
    act = idx[2:]
    chain = act.copy()
    while act.size:
        omega[act] += 1
        chain = rest[chain]
        keep = chain > 1
        act = act[keep]
        chain = chain[keep]

    total = 0  # M(1) = 0 contributes nothing

    # Round 1: prime powers have idempotents {0, 1}, so M = 1.
    pos = np.zeros(N + 1, dtype=np.int32)
    ns = idx[omega == 1]
    pos[ns] = np.arange(ns.size, dtype=np.int32)
    idem_prev = np.zeros((ns.size, 2), dtype=np.int32)
    idem_prev[:, 1] = 1
    total += ns.size

    for k in range(2, int(omega.max()) + 1):
        ns = idx[omega == k]
        qk = q[ns]
        m = ns // qk
        prev = idem_prev[pos[m]].astype(np.int64)  # shape (count, 2^(k-1))

        # minv = m^{-1} mod qk via Euler: exponent phi(qk) - 1 = qk - qk/p - 1.
        e = qk - qk // spf64[ns] - 1
        b = m % qk
        minv = np.ones_like(qk)
        while e.max() > 0:
            sel = (e & 1) == 1
            minv[sel] = minv[sel] * b[sel] % qk[sel]
            b = b * b % qk
            e >>= 1

        # CRT lift: x = e + m * ((t - e) * minv mod qk) for t in {0, 1}.
        mm = m[:, None]
        qq = qk[:, None]
        iv = minv[:, None]
        x0 = prev + mm * ((-prev) * iv % qq)
        x1 = prev + mm * ((1 - prev) * iv % qq)
        idem = np.concatenate([x0, x1], axis=1)

        total += int(idem.max(axis=1).sum())
        pos[ns] = np.arange(ns.size, dtype=np.int32)
        idem_prev = idem.astype(np.int32)

    return total


if __name__ == "__main__":
    print(solve())
