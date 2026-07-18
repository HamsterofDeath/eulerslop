#!/usr/bin/env python3
"""Project Euler 909: normalize the L-expression."""

LAST_DIGITS_MODULUS = 10**9


def h(number: int) -> int:
    """Integer action of H = S(S(S))(S(S)).

    Regard Z as Church numeral N_0.  The given S maps N_n to N_(n+1).
    Put X=S(S).  Direct substitution in the reduction rule gives

        X(N_n) = N_(n(n+1)).

    For Y=X(X), set m=n^2(n+1); then

        Y(N_n) = N_(m(m+1)).

    Finally H=S(X)(X) applies X once more to Y(N_n), producing the
    polynomial below.
    """
    m = number * number * (number + 1)
    y = m * (m + 1)
    return y * (y + 1)


def normalized_value() -> int:
    """Return the full natural number represented by the expression."""
    # With N_1=S(Z), the expression before A(0) is
    #
    #   X(X)(X)(N_1) = H(H(N_1)).
    return h(h(1))


def solve() -> int:
    assert h(1) == 42
    assert normalized_value() == 33_103_933_172_399_885_292
    return normalized_value() % LAST_DIGITS_MODULUS


if __name__ == "__main__":
    print(solve())
