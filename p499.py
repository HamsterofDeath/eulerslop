#!/usr/bin/env python3

import math


def root_equation(r, fee):
    if r <= 0.0:
        return -0.5
    log_r = math.log(r)
    total = 0.0
    probability = 0.5
    payout = 1
    while probability > 1e-320:
        exponent = payout * log_r
        if exponent < -750:
            break
        total += probability * math.exp(exponent)
        probability *= 0.5
        payout *= 2
    return r**fee - total


def ruin_root(fee):
    low = 0.0
    high = 1.0
    # The nontrivial root is very close to 1 for larger fees.  Move the lower
    # bound up until the sign changes away from the trivial root at r = 1.
    for exponent in range(1, 20):
        candidate = 1.0 - 10.0 ** (-exponent)
        if root_equation(candidate, fee) < 0:
            low = candidate
        else:
            high = candidate
            break

    for _ in range(200):
        mid = (low + high) / 2
        if root_equation(mid, fee) < 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def survival_probability(fee, fortune):
    r = ruin_root(fee)
    ruin = math.exp((fortune - fee + 1) * math.log(r))
    return 1.0 - ruin


def solve():
    assert f"{survival_probability(2, 2):.4f}" == "0.2522"
    assert f"{survival_probability(2, 5):.4f}" == "0.6873"
    assert f"{survival_probability(6, 10_000):.4f}" == "0.9952"
    return f"{survival_probability(15, 10**9):.7f}"


if __name__ == "__main__":
    print(solve())
