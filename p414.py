import numpy as np


def S_of_b(b):
    # Kaprekar step on a 5-digit base-b number with sorted digits a>=p>=q>=r>=e:
    # desc - asc = x*b^4 + y*b^3 - y*b - x with x = a-e, y = p-r, so one step
    # collapses everything to the O(b^2) state (x, y), 0 <= y <= x <= b-1.
    n = b * b
    idx = np.arange(n, dtype=np.int64)
    x = idx // b
    y = idx % b
    valid = (y <= x) & (x >= 1)  # x == 0 <=> repdigit (sb = 0)

    # Digits of v = f(x,y) = x*b^4 + y*b^3 - y*b - x:
    #   y >= 1: (x, y-1, b-1, b-1-y, b-x);  y == 0: (x-1, b-1, b-1, b-1, b-x)
    yz = (y == 0)
    digs = np.stack([
        np.where(yz, x - 1, x),
        np.where(yz, b - 1, y - 1),
        np.full(n, b - 1, dtype=np.int64),
        np.where(yz, b - 1, b - 1 - y),
        b - x,
    ], axis=1)
    digs.sort(axis=1)
    nxt = (digs[:, 4] - digs[:, 0]) * b + (digs[:, 3] - digs[:, 1])

    # Unique valid fixed point s* satisfies f(s*) = C_b (Kaprekar constant).
    fp = np.nonzero(valid & (nxt == idx))[0]
    assert len(fp) == 1
    s_star = int(fp[0])
    nxt = np.where(valid, nxt, s_star)
    nxt[s_star] = s_star

    # D[s] = steps from value f(s) to C_b, via pointer doubling.
    dacc = np.where(valid, 1, 0).astype(np.int64)
    dacc[s_star] = 0
    while True:
        new = dacc + dacc[nxt]
        nxt = nxt[nxt]
        if np.array_equal(new, dacc):
            break
        dacc = new

    # N(x,y) = #numbers in [0,b^5) whose 5-digit string has state (x,y).
    # With u = r-e in [0,x-y], v = q-r in [0,y] and free min digit e (b-x
    # choices), the permutation multinomial depends only on boundary flags;
    # summing it over (u,v) in closed form:
    Wgen = 100 + 120 * ((x - 2) + (x - y - 1) * (y - 1))
    W = np.where(yz, 20 * x - 10, np.where(y == x, 30 * x - 10, Wgen))
    Ncnt = np.where(valid, (b - x) * W, 0)

    # sb(i) = 1 + D[state(i)] for non-repdigit i, except sb(C_b) = 0 (its term
    # above is 1 + D[s*] = 1, hence the trailing -1).
    rows = (Ncnt * (1 + dacc)).reshape(b, b).sum(axis=1)
    return sum(int(v) for v in rows) - 1


def solve():
    # Self-check against the values given in the problem statement.
    assert S_of_b(15) == 5274369
    assert S_of_b(111) == 400668930299
    total = sum(S_of_b(6 * k + 3) for k in range(2, 301))
    return total % 10**18  # last 18 digits


if __name__ == "__main__":
    print(solve())
