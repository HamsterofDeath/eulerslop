"""Project Euler Problem 921: A Golden-Ratio Recurrence.

The rational function is the fifth-angle formula for tanh.  It follows that,
for k = 5^n,

    (2 + sqrt(5))^k = A_k + B_k*sqrt(5)
    a_n = (1 + B_k*sqrt(5)) / A_k.

Hence p_n = B_k and q_n = A_k.  Modulo the prime 398874989, sqrt(5) exists
and the quadratic ring splits into two scalar field embeddings.  Their
combined exponent order is 2*99718747.

Finally, e_i = 5^F_i obeys e_i = e_(i-1)*e_(i-2) modulo that order, allowing
the Fibonacci-indexed sum to be accumulated directly.
"""


MODULUS = 398_874_989
ORDER_COMPONENT = 99_718_747
EXPONENT_MODULUS = 2 * ORDER_COMPONENT
TARGET = 1_618_034


def square_root_of_five() -> int:
    """Return a square root of five modulo MODULUS (which is 5 mod 8)."""
    root = pow(5, (MODULUS + 3) // 8, MODULUS)
    if root * root % MODULUS != 5:
        root = root * pow(2, (MODULUS - 1) // 4, MODULUS) % MODULUS
    assert root * root % MODULUS == 5
    return root


ROOT_FIVE = square_root_of_five()
PLUS_EMBEDDING = (2 + ROOT_FIVE) % MODULUS
MINUS_EMBEDDING = (2 - ROOT_FIVE) % MODULUS
INVERSE_TWO = (MODULUS + 1) // 2
INVERSE_TWO_ROOT = pow(2 * ROOT_FIVE, MODULUS - 2, MODULUS)


def sequence_value_from_exponent(exponent: int) -> int:
    """Return s(n) when exponent = 5^n modulo EXPONENT_MODULUS."""
    plus_power = pow(PLUS_EMBEDDING, exponent, MODULUS)
    minus_power = pow(
        MINUS_EMBEDDING,
        exponent % ORDER_COMPONENT,
        MODULUS,
    )

    q_value = (plus_power + minus_power) * INVERSE_TWO % MODULUS
    p_value = (plus_power - minus_power) * INVERSE_TWO_ROOT % MODULUS
    return (pow(p_value, 5, MODULUS) + pow(q_value, 5, MODULUS)) % MODULUS


def fibonacci_index_sum(count: int) -> int:
    # F_1 = F_2 = 1, so the first two exponent residues are both 5.
    previous_exponent = 5
    exponent = 5
    result = sequence_value_from_exponent(exponent)  # i = 2

    for _ in range(3, count + 1):
        previous_exponent, exponent = (
            exponent,
            previous_exponent * exponent % EXPONENT_MODULUS,
        )
        result = (result + sequence_value_from_exponent(exponent)) % MODULUS

    return result


def solve() -> int:
    assert sequence_value_from_exponent(1) == 33
    return fibonacci_index_sum(TARGET)


if __name__ == "__main__":
    print(solve())
