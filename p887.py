#!/usr/bin/env python3
"""Project Euler 887: capacity of depth-constrained search trees."""


LIMIT = 7**10


def capacity(question_limit: int, allowance: int) -> int:
    """Maximum N searchable with at most question_limit questions.

    The ordered leaves form an alphabetic binary prefix code.  Giving
    leaf x its deepest permitted depth min(q, x+d) minimizes its Kraft
    weight and therefore maximizes the number of leaves.
    """
    if question_limit <= allowance + 1:
        return 1 << question_limit
    return (
        (1 << question_limit)
        - (1 << (question_limit - allowance))
        + question_limit
        - allowance
        + 1
    )


def minimum_questions(number_count: int, allowance: int) -> int:
    if allowance == 0:
        return number_count - 1
    questions = 0
    while capacity(questions, allowance) < number_count:
        questions += 1
    return questions


def summatory_questions(number_limit: int, allowance: int) -> int:
    """Sum Q(N, allowance) for 1 <= N <= number_limit."""
    if allowance == 0:
        return number_limit * (number_limit - 1) // 2

    # Q(N,d)>q exactly when N exceeds the capacity at depth q.
    result = 0
    questions = 0
    while capacity(questions, allowance) < number_limit:
        result += number_limit - capacity(questions, allowance)
        questions += 1
    return result


def solve() -> int:
    assert minimum_questions(7, 1) == 3
    assert minimum_questions(777, 2) == 10
    return sum(
        summatory_questions(LIMIT, allowance)
        for allowance in range(8)
    )


if __name__ == "__main__":
    print(solve())
