#!/usr/bin/env python3
"""Project Euler 672: a base-seven summatory recurrence."""


MOD = 1_117_117_717
K = 1_000_000_000
BLOCK = (4, 3, 1, 1, 6, 2, 3, 5, 5, 0)


def _digit_matrix(digit: int) -> list[list[int]]:
    constant = -6 + 7 * digit - digit * (digit + 1) // 2
    carry_cost = 0 if digit == 6 else 6 - digit
    return [
        [7, digit, 21, constant % MOD],
        [0, 1, 0, carry_cost],
        [0, 0, 7, digit],
        [0, 0, 0, 1],
    ]


def _mat_mul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(left[row][i] * right[i][col] for i in range(4)) % MOD
            for col in range(4)
        ]
        for row in range(4)
    ]


def _mat_pow(matrix: list[list[int]], exponent: int) -> list[list[int]]:
    result = [[int(row == col) for col in range(4)] for row in range(4)]
    while exponent:
        if exponent & 1:
            result = _mat_mul(result, matrix)
        matrix = _mat_mul(matrix, matrix)
        exponent >>= 1
    return result


def _sequence_matrix(digits: tuple[int, ...]) -> list[list[int]]:
    result = [[int(row == col) for col in range(4)] for row in range(4)]
    for digit in digits:
        result = _mat_mul(_digit_matrix(digit), result)
    return result


def _apply(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        sum(matrix[row][col] * vector[col] for col in range(4)) % MOD
        for row in range(4)
    ]


def solve(k: int = K) -> int:
    if k % 10 != 0:
        raise ValueError("the Project Euler input has K divisible by 10")

    periods = k // 10
    state = [12, 2, 4, 1]
    if periods == 1:
        return _apply(_sequence_matrix(BLOCK[1:-1]), state)[0]

    state = _apply(_sequence_matrix(BLOCK[1:]), state)
    state = _apply(_mat_pow(_sequence_matrix(BLOCK), periods - 2), state)
    state = _apply(_sequence_matrix(BLOCK[:-1]), state)
    return state[0]


if __name__ == "__main__":
    print(solve())
