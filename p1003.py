#!/usr/bin/env python3
"""Project Euler Problem 1003: Lonely Singles.

With m_j stones at position j (m_0 = n) the counts satisfy

    m_j = floor(m_{j-1} / 2) + floor(m_{j-3} / 2),

and a singleton is left at j exactly when m_j is odd.  Every sequence
eventually becomes a constant even value c = 2t, so singletons are finite
and the parity pattern a_j = m_j mod 2 eventually vanishes.  Writing
m_j = 2t + u_j, the deviations u_j obey the linear recurrence

    u_{j-3} = 2*u_j - u_{j-1} + a_{j-1} + a_{j-3},

so u_j (and therefore n = m_0) is a fixed linear functional of the
pattern.  With h(d) the impulse response (h(0)=1, h(1)=h(2)=0,
h(d) = 2h(d-3) - h(d-2)) a pattern a_0..a_{k-1} corresponds to a valid n
iff the boundary relations at positions 1 and 2 hold, i.e.

    sum_j gamma_j a_j = 0,   gamma_j = h(j) - 3h(j-1) + 2h(j-2) - [j=0] + [j=1]
    2t = sum_j tau_j a_j >= 0,   tau_j = h(j-1) - 2h(j-2) - [j=1]
    m_2 = sum_j mu_j a_j >= 0,   mu_j = h(j-1) - h(j-2) - [j=1]
    n  = sum_j W_j a_j >= 1,     W_j = h(j) + h(j-1) - 2h(j-2) - [j=1]

The lonely patterns (1s at pairwise distance >= 3) are searched with a
depth-first search that fixes high-index bits first and prunes a prefix
when the residual of one of the four sums cannot be repaired by the
remaining bits (bounds via prefix sums of absolute values / positive
parts).
"""


def _sad_sum(k):
    h = [0] * (2 * k + 2)
    h[0] = 1
    h[1] = 0
    h[2] = 0
    for d in range(3, len(h)):
        h[d] = 2 * h[d - 3] - h[d - 2]

    def hh(d):
        return h[d] if d >= 0 else 0

    gamma = [hh(j) - 3 * hh(j - 1) + 2 * hh(j - 2) - (j == 0) + (j == 1)
             for j in range(k)]
    tau = [hh(j - 1) - 2 * hh(j - 2) - (j == 1) for j in range(k)]
    mu = [hh(j - 1) - hh(j - 2) - (j == 1) for j in range(k)]
    weight = [hh(j) + hh(j - 1) - 2 * hh(j - 2) - (j == 1)
              for j in range(k)]

    abs_gamma = [abs(x) for x in gamma]
    pos_tau = [max(0, x) for x in tau]
    pos_mu = [max(0, x) for x in mu]
    pos_w = [max(0, x) for x in weight]
    for arr in (abs_gamma, pos_tau, pos_mu, pos_w):
        acc = 0
        for i in range(k):
            acc += arr[i]
            arr[i] = acc

    def bounds(i):
        # max |residual|, max future contribution to t, m_2, n over bits < i
        if i <= 0:
            return 0, 0, 0, 0
        return abs_gamma[i - 1], pos_tau[i - 1], pos_mu[i - 1], pos_w[i - 1]

    total = 0

    def dfs(i, b1, b2, res, t_part, m2_part, n_part):
        nonlocal total
        if i < 0:
            if res == 0 and t_part >= 0 and m2_part >= 0 and n_part >= 1:
                total += n_part
            return
        g_lim, t_lim, m_lim, n_lim = bounds(i + 1)
        if res + g_lim < 0 or res - g_lim > 0:
            return
        if t_part + t_lim < 0:
            return
        if m2_part + m_lim < 0:
            return
        if n_part + n_lim < 1:
            return
        dfs(i - 1, 0, b1, res, t_part, m2_part, n_part)
        if b1 == 0 and b2 == 0:
            dfs(i - 1, 1, b1, res + gamma[i], t_part + tau[i],
                m2_part + mu[i], n_part + weight[i])

    dfs(k - 1, 0, 0, 0, 0, 0, 0)
    return total


def solve() -> int:
    return _sad_sum(80)


if __name__ == "__main__":
    print(solve())
