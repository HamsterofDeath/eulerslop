#!/usr/bin/env python3


M = 904_961


def _sum_v2_factorial(n):
    return n - n.bit_count()


def Q(n):
    # For N=(p_m#)^e, divisor pairs a|b are coordinate pairs alpha<=beta in
    # [0,e]^m, except equal pairs:
    # S(N)=(((e+1)(e+2)/2)^m - (e+1)^m).
    #
    # With m odd, compare the 2-adic valuations of A=(e+1)(e+2)/2 and B=e+1.
    odd_terms = (n + 1) // 2
    multiple_of_four_terms = n // 4
    return (
        M * _sum_v2_factorial(odd_terms)
        + multiple_of_four_terms
        + _sum_v2_factorial(multiple_of_four_terms)
    )


def solve():
    assert Q(8) == 2714886
    return Q(10 ** 12)


if __name__ == "__main__":
    print(solve())
