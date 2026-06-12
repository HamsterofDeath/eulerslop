#!/usr/bin/env python3

MOD = 1_000_000_007


def digit_matrices(base, depth):
    matrices = []
    for digit in range(base):
        matrix = [[0] * (depth + 1) for _ in range(depth + 1)]
        matrix[0][0] = digit + 1 - base
        matrix[0][1] = base
        matrices.append(matrix)

    for row_index in range(1, depth + 1):
        complete = [0] * (depth + 1)
        for digit in range(base):
            row = matrices[digit][row_index - 1]
            for col, value in enumerate(row):
                complete[col] = (complete[col] + value) % MOD

        partial = [0] * (depth + 1)
        for digit in range(base):
            previous_row = matrices[digit][row_index - 1]
            for col, value in enumerate(previous_row):
                partial[col] = (partial[col] + value) % MOD

            row = matrices[digit][row_index]
            for col in range(depth + 1):
                row[col] = (row[col] + partial[col] - complete[col]) % MOD
                if col + 1 <= depth:
                    row[col + 1] = (row[col + 1] + complete[col]) % MOD

    return matrices


def f(base, n):
    if n == 0:
        return 1

    digits = []
    x = n
    while x:
        digits.append(x % base)
        x //= base
    digits.reverse()

    depth = len(digits)
    matrices = digit_matrices(base, depth)
    values = [1] * (depth + 1)

    for digit in digits:
        matrix = matrices[digit]
        values = [
            sum(matrix[row][col] * values[col] for col in range(depth + 1)) % MOD
            for row in range(depth + 1)
        ]

    return values[0]


def solve():
    assert f(5, 10) == 18
    assert f(7, 100) == 1003
    assert f(2, 10**3) == 264830889564 % MOD
    return sum(f(k, 10**14) for k in range(2, 11)) % MOD


if __name__ == "__main__":
    print(solve())
