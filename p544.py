#!/usr/bin/env python3

MOD = 1_000_000_007


def canonical(state):
    seen = {}
    result = []
    for label in state:
        if label not in seen:
            seen[label] = len(seen)
        result.append(seen[label])
    return tuple(result)


def add_poly(target, source, sign=1):
    if len(target) < len(source):
        target.extend([0] * (len(source) - len(target)))
    if sign == 1:
        for i, value in enumerate(source):
            target[i] = (target[i] + value) % MOD
    else:
        for i, value in enumerate(source):
            target[i] = (target[i] - value) % MOD


def chromatic_polynomial(rows, cols):
    """Return coefficients of the grid chromatic polynomial modulo MOD."""
    frontier = []
    positions = {}
    states = {(): [1]}

    def rebuild_positions():
        positions.clear()
        positions.update({vertex: i for i, vertex in enumerate(frontier)})

    def add_vertex(vertex):
        nonlocal states
        next_states = {}
        for state, poly in states.items():
            label = max(state) + 1 if state else 0
            next_states[state + (label,)] = poly[:]
        frontier.append(vertex)
        positions[vertex] = len(frontier) - 1
        states = next_states

    def union_state(state, i, j):
        if state[i] == state[j]:
            return None
        keep = state[i]
        remove = state[j]
        merged = [keep if label == remove else label for label in state]
        return canonical(merged)

    def process_edge(a, b):
        nonlocal states
        i = positions[a]
        j = positions[b]
        next_states = {}
        for state, poly in states.items():
            if state not in next_states:
                next_states[state] = [0] * len(poly)
            add_poly(next_states[state], poly)

            merged = union_state(state, i, j)
            if merged is None:
                add_poly(next_states[state], poly, -1)
            else:
                if merged not in next_states:
                    next_states[merged] = [0] * len(poly)
                add_poly(next_states[merged], poly, -1)
        states = {state: poly for state, poly in next_states.items() if any(poly)}

    def forget_vertex(vertex):
        nonlocal states
        index = positions[vertex]
        next_states = {}
        for state, poly in states.items():
            label = state[index]
            reduced = canonical(state[:index] + state[index + 1 :])
            closed_poly = [0] + poly if state.count(label) == 1 else poly[:]
            if reduced not in next_states:
                next_states[reduced] = [0] * len(closed_poly)
            add_poly(next_states[reduced], closed_poly)
        frontier.pop(index)
        rebuild_positions()
        states = next_states

    for row in range(rows):
        for col in range(cols):
            vertex = (row, col)
            add_vertex(vertex)
            if col:
                process_edge((row, col - 1), vertex)
            if row:
                process_edge((row - 1, col), vertex)
                forget_vertex((row - 1, col))

    for col in range(cols):
        forget_vertex((rows - 1, col))

    return states[()]


def evaluate(poly, x):
    result = 0
    for coeff in reversed(poly):
        result = (result * x + coeff) % MOD
    return result


def interpolate_at(values, x):
    degree = len(values) - 1
    if x <= degree:
        return values[x]

    prefix = [1] * (degree + 2)
    suffix = [1] * (degree + 2)
    for i in range(degree + 1):
        prefix[i + 1] = prefix[i] * (x - i) % MOD
    for i in range(degree, -1, -1):
        suffix[i] = suffix[i + 1] * (x - i) % MOD

    factorial = [1] * (degree + 1)
    inv_factorial = [1] * (degree + 1)
    for i in range(1, degree + 1):
        factorial[i] = factorial[i - 1] * i % MOD
    inv_factorial[degree] = pow(factorial[degree], MOD - 2, MOD)
    for i in range(degree, 0, -1):
        inv_factorial[i - 1] = inv_factorial[i] * i % MOD

    result = 0
    for i, value in enumerate(values):
        numerator = prefix[i] * suffix[i + 1] % MOD
        denominator = inv_factorial[i] * inv_factorial[degree - i] % MOD
        if (degree - i) & 1:
            denominator = -denominator
        result = (result + value * numerator * denominator) % MOD
    return result % MOD


def summed_grid_colourings(rows, cols, limit):
    poly = chromatic_polynomial(rows, cols)
    prefix_values = []
    total = 0
    for x in range(len(poly) + 1):
        if x:
            total = (total + evaluate(poly, x)) % MOD
        prefix_values.append(total)
    return interpolate_at(prefix_values, limit)


def solve():
    square = chromatic_polynomial(2, 2)
    assert evaluate(square, 3) == 18
    assert evaluate(square, 20) == 130340
    assert evaluate(chromatic_polynomial(3, 4), 6) == 102923670
    assert summed_grid_colourings(4, 4, 15) == 325951319
    return str(summed_grid_colourings(9, 10, 1_112_131_415))


if __name__ == "__main__":
    print(solve())
