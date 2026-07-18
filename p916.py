"""Project Euler Problem 916: Permutations and Subsequences.

By RSK, the permutations are counted by pairs of standard Young tableaux.
The decreasing-subsequence condition allows at most two rows, while the
increasing-subsequence condition leaves only the shapes (n,n) and
(n+1,n-1).  The hook-length formula therefore gives

    P(n) = Catalan(n)^2 * (1 + (3n/(n+2))^2).

The large central binomial coefficient is evaluated with constant-memory
blocks of pairwise NumPy uint64 products.  Every intermediate is reduced
modulo 1e9+7, whose squared residues fit safely in uint64.
"""

import numpy as np


MODULUS = 1_000_000_007
MODULUS_UINT64 = np.uint64(MODULUS)
TARGET = 10**8
BLOCK_SIZE = 1_000_000


def range_product(lower: int, upper: int) -> int:
    """Return the inclusive range product modulo MODULUS."""
    result = 1

    for start in range(lower, upper + 1, BLOCK_SIZE):
        stop = min(start + BLOCK_SIZE, upper + 1)
        values = np.arange(start, stop, dtype=np.uint64)

        while values.size > 1:
            even_size = values.size - (values.size & 1)
            products = (
                values[:even_size:2] * values[1:even_size:2]
            ) % MODULUS_UINT64
            if even_size < values.size:
                products[0] = products[0] * values[-1] % MODULUS_UINT64
            values = products

        result = result * int(values[0]) % MODULUS

    return result


def permutation_count(n: int) -> int:
    numerator = range_product(n + 1, 2 * n)
    denominator = range_product(1, n)
    central_binomial = (
        numerator * pow(denominator, MODULUS - 2, MODULUS) % MODULUS
    )
    catalan = central_binomial * pow(n + 1, MODULUS - 2, MODULUS) % MODULUS

    second_shape_ratio = (
        3 * n % MODULUS * pow(n + 2, MODULUS - 2, MODULUS) % MODULUS
    )
    shape_factor = (1 + second_shape_ratio * second_shape_ratio) % MODULUS
    return catalan * catalan % MODULUS * shape_factor % MODULUS


def solve() -> int:
    assert permutation_count(2) == 13
    assert permutation_count(10) == 45_265_702
    return permutation_count(TARGET)


if __name__ == "__main__":
    print(solve())
