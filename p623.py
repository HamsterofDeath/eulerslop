#!/usr/bin/env python3
"""Project Euler 623: count closed lambda terms by de Bruijn context size."""


MOD = 1_000_000_007
N = 2000


def solve(n=N, mod=MOD):
    # L_m(z) counts terms whose free variables may refer to any of m enclosing
    # binders: L_m = m*z + z^2*L_m^2 + z^5*L_{m+1}.
    max_context = (n - 1) // 5
    next_counts = [0]

    for context in range(max_context, -1, -1):
        limit = n - 5 * context
        counts = [0] * (limit + 1)

        for size in range(1, limit + 1):
            value = context if size == 1 else 0

            child_total = size - 2
            if child_total >= 2:
                convolution = 0
                half = child_total // 2
                for left in range(1, half + 1):
                    right = child_total - left
                    if left == right:
                        convolution += counts[left] * counts[left]
                    else:
                        convolution += 2 * counts[left] * counts[right]
                value += convolution

            if size >= 6:
                value += next_counts[size - 5]

            counts[size] = value % mod

        next_counts = counts

    return sum(next_counts) % mod


if __name__ == "__main__":
    print(solve())
