#!/usr/bin/env python3
import math

def P(f, r):
    # Closed form, derived from simulating the assignment process:
    # the occupants a_1, a_2, ... of floor f satisfy a_k + a_{k+1} = (k+s)^2
    # with s = 1 for f = 1 and s = 2*floor(f/2) otherwise, and first occupant
    # a_1 = 1 (f=1), f^2/2 (f even), (f^2-1)/2 (f odd >= 3).
    # From a_{k+2} - a_k = (k+1+s)^2 - (k+s)^2 = 2k + 2s + 1, summing gives a
    # quadratic in the room index for each parity of r.
    if f == 1:
        a1, s = 1, 1
    elif f % 2 == 0:
        a1, s = f * f // 2, f
    else:
        a1, s = (f * f - 1) // 2, f - 1
    if r % 2 == 1:
        j = (r - 1) // 2
        return a1 + 2 * j * j + j * (2 * s + 1)
    j = r // 2
    return (1 + s) ** 2 - a1 + 2 * j * (j - 1) + (j - 1) * (2 * s + 1)

def simulate(npeople):
    # direct simulation of Hilbert's rule, for validating the closed form
    floors = []
    for n in range(1, npeople + 1):
        for fl in floors:
            t = math.isqrt(fl[-1] + n)
            if t * t == fl[-1] + n:
                fl.append(n)
                break
        else:
            floors.append([n])
    return floors

def solve():
    # Validate the closed form against a brute-force simulation and the
    # examples given in the problem statement.
    for f, fl in enumerate(simulate(5000), 1):
        for r, person in enumerate(fl, 1):
            assert P(f, r) == person, (f, r)
    assert (P(1, 1), P(1, 2), P(2, 1)) == (1, 3, 2)
    assert (P(10, 20), P(25, 75), P(99, 100)) == (440, 4863, 19454)

    # Sum P(f, r) over all factorizations f*r = N, mod 10^8.
    N = 71328803586048  # = 2^27 * 3^12
    divisors, n, p = [1], N, 2
    while n > 1:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            divisors = [d * p ** k for d in divisors for k in range(e + 1)]
        p += 1
    return sum(P(f, N // f) for f in divisors) % 10 ** 8

if __name__ == "__main__":
    print(solve())
