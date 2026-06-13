#!/usr/bin/env python3
from collections import defaultdict

MOD = 1_000_000_007
N = 10**18
M = 40
INF = 10**9


def prefix_data(p):
    """Prefix minima, first increasing-pair threshold, and suffix maxima."""
    n = len(p)
    pref_min = [INF] * (n + 1)
    pref_pair = [INF] * (n + 1)
    mn = INF
    pair = INF
    for i, v in enumerate(p, 1):
        if mn < v < pair:
            pair = v
        if v < mn:
            mn = v
        pref_min[i] = mn
        pref_pair[i] = pair

    suffix_max = [0] * (n + 1)
    mx = 0
    for i in range(n - 1, -1, -1):
        if p[i] > mx:
            mx = p[i]
        suffix_max[i] = mx
    return pref_min, pref_pair, suffix_max


def tau_with_fixed_tail(length, fixed_count, pref_min, pref_pair):
    """Increasing-pair threshold after appending fixed values length+1, ... ."""
    pair = pref_pair[length]
    if pair != INF:
        return pair
    if fixed_count == 0:
        return INF
    if pref_min[length] != INF:
        return length + 1
    if fixed_count >= 2:
        return length + 2
    return INF


def solve(limit=N, max_inv=M):
    # The empty core represents the identity permutation in every length.
    answer = (limit + 1) % MOD

    layers = [[] for _ in range(max_inv + 1)]
    layers[0].append(())

    for inv in range(max_inv):
        current = layers[inv]
        if not current:
            continue
        remaining = max_inv - inv

        for p in current:
            length = len(p)
            pref_min, pref_pair, suffix_max = prefix_data(p)

            for added_inv in range(1, remaining + 1):
                # Append z fixed points before the positive insertion.  If
                # z > added_inv + 1, two fixed values before the new maximum
                # and a fixed value after it force a 1243 occurrence.
                first_z = max(0, added_inv - length)
                last_z = added_inv + 1

                for z in range(first_z, last_z + 1):
                    extended_length = length + z
                    cut = extended_length - added_inv

                    if z:
                        if cut <= length:
                            pair = pref_pair[cut]
                        else:
                            pair = tau_with_fixed_tail(
                                length, cut - length, pref_min, pref_pair
                            )
                        # Any appended fixed value after the new maximum is
                        # larger than a finite threshold, so it would be the
                        # final "3" in a newly-created 1243.
                        if pair != INF:
                            continue
                    else:
                        pair = pref_pair[cut]
                        if pair != INF and suffix_max[cut] > pair:
                            continue

                    new_value = extended_length + 1
                    if z == 0:
                        child = p[:cut] + (new_value,) + p[cut:]
                    else:
                        fixed = tuple(range(length + 1, extended_length + 1))
                        if cut <= length:
                            child = p[:cut] + (new_value,) + p[cut:] + fixed
                        else:
                            fixed_cut = cut - length
                            child = (
                                p
                                + fixed[:fixed_cut]
                                + (new_value,)
                                + fixed[fixed_cut:]
                            )

                    layers[inv + added_inv].append(child)
                    if len(child) <= limit:
                        answer = (answer + limit - len(child) + 1) % MOD

        layers[inv] = []

    return answer


if __name__ == "__main__":
    print(solve())
