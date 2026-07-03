#!/usr/bin/env python3
"""Project Euler 809: rational recursion reduced to iterated maps."""


MOD = 10**15


def fixed_point_mod(modulus: int) -> int:
    """Fixed point of x -> 8*2^x - 3 reached by iterating from 13."""
    x = 13 % modulus
    while True:
        y = (8 * pow(2, x, modulus) - 3) % modulus
        if y == x:
            return x
        x = y


def a_q_one_over_d(q: int, d: int) -> int:
    if d == 1:
        return q + 1
    if d == 2:
        return q + 2
    if d == 3:
        return 2 * q + 3
    if d == 4:
        return 8 * 2**q - 3
    raise ValueError("exact helper is only needed for small sample depths")


def solve() -> int:
    # For A(q,d)=f(q+1/d):
    # A(q,1)=q+1, A(0,d)=A(1,d-1), A(q,d)=A(A(q-1,d),d-1).
    # This gives f(3/2)=A(1,2)=3 and f(1/6)=A(1,5)=8*2^13-3.
    assert a_q_one_over_d(1, 2) == 3
    assert a_q_one_over_d(a_q_one_over_d(1, 4), 4) == 65533

    # The 13/10 example reduces to B(q)=f(q+3/7),
    # B(0)=7, B(q)=3*B(q-1)+4, evaluated at q=25.
    assert 9 * 3**25 - 2 == 7625597484985

    # 22/7 = 3 + 1/7.  From depth 5 onward the recurrence iterates
    # x -> 8*2^x - 3, which has stabilized modulo 10^15 long before the
    # huge iteration counts produced by A(3,7).
    return fixed_point_mod(MOD)


if __name__ == "__main__":
    print(solve())
