#!/usr/bin/env python3

def solve():
    # Plate numbers are uniform on 0..999.  Plate 0 can never contribute (no
    # plate 1000 exists).  Plate 500 wins only with another 500.  The other 998
    # numbers form 499 complement classes {k, 1000-k}; once one member of a
    # class has been seen, seeing the other member wins (seeing the same member
    # again changes nothing).
    #
    # State (n, s): n = number of classes with one member seen (0..499),
    # s = 1 if a 500 has been seen.  Next plate:
    #   1/1000          -> 0, no change
    #   n/1000          -> repeat of a seen member, no change
    #   n/1000          -> complement of a seen member, WIN
    #   1/1000          -> 500: win if s=1, else move to s=1
    #   (998-2n)/1000   -> fresh class, n -> n+1
    # Solve E(n,s) = 1 + (stay)E(n,s) + (transitions) backwards from n=499.
    E1 = [0.0] * 500  # E(n, 500 already seen)
    E0 = [0.0] * 500  # E(n, 500 not yet seen)

    # n = 499: no fresh classes remain.
    E1[499] = 1 / (1 - 500 / 1000)                       # win prob 500/1000
    for n in range(498, -1, -1):
        E1[n] = (1 + (998 - 2 * n) / 1000 * E1[n + 1]) / (1 - (n + 1) / 1000)

    E0[499] = (1 + E1[499] / 1000) / (1 - 500 / 1000)
    for n in range(498, -1, -1):
        E0[n] = (1 + E1[n] / 1000 + (998 - 2 * n) / 1000 * E0[n + 1]) \
                / (1 - (n + 1) / 1000)

    return f"{E0[0]:.8f}"

if __name__ == "__main__":
    print(solve())
