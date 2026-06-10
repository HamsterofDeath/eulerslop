#!/usr/bin/env python3

def solve():
    # Count "barely obtuse" triangles a <= b <= c with a^2 + b^2 = c^2 - 1
    # and perimeter a + b + c <= 75,000,000.
    #
    # All solutions form a ternary tree rooted at (2, 2, 3) under the three
    # classic Pythagorean-tree matrices (they preserve a^2 + b^2 - c^2 = -1):
    #   (a, b, c) -> ( a - 2b + 2c,  2a - b + 2c,  2a - 2b + 3c)
    #   (a, b, c) -> ( a + 2b + 2c,  2a + b + 2c,  2a + 2b + 3c)
    #   (a, b, c) -> (-a + 2b + 2c, -2a + b + 2c, -2a + 2b + 3c)
    # The tree enumerates ordered pairs (a, b); at nodes with a == b (Pell
    # solutions 2a^2 = c^2 - 1) the first and third branches are mirror
    # images, so one of them is skipped to count each unordered triangle
    # exactly once (verified against brute force for small perimeters).
    limit = 75_000_000
    count = 0
    stack = [(2, 2, 3)]
    push = stack.append
    pop = stack.pop
    while stack:
        a, b, c = pop()
        if a + b + c > limit:
            continue
        count += 1
        c2 = 2 * c
        push((a - 2 * b + c2, 2 * a - b + c2, 2 * a - 2 * b + 3 * c))
        push((a + 2 * b + c2, 2 * a + b + c2, 2 * a + 2 * b + 3 * c))
        if a != b:
            push((2 * b - a + c2, b - 2 * a + c2, 2 * b - 2 * a + 3 * c))
    return count

if __name__ == "__main__":
    print(solve())
