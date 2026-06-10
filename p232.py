#!/usr/bin/env python3

def solve():
    TARGET = 100

    # W[a][b] = probability Player 2 wins when Player 1 needs a more points,
    # Player 2 needs b more points, and Player 1 is about to toss.
    # A round: Player 1 tosses (heads 1/2 -> scores 1), then Player 2 picks T
    # and tosses (all heads, prob p = 2^-T -> scores s = 2^(T-1)).
    #
    # Let V(a', b) = value when Player 2 is about to toss and Player 1 needs a'
    # (a' = 0 means Player 1 already won, value 0):
    #   V(a', b) = max_T [ p * (1 if b <= s else W[a'][b-s]) + (1-p) * W_self ]
    # where the (1-p) branch returns to the top of the round in the same state
    # only when a' == a (Player 1 failed too). Writing the round equation:
    #   W[a][b] = 1/2 * V(a-1, b) + 1/2 * V(a, b)
    # and V(a, b)'s failure branch loops back to W[a][b]. For a fixed T:
    #   W = 1/2*A + 1/2*(p*w + (1-p)*W)   with A = V(a-1, b)
    # => W_T = (A + p*w) / (1 + p), and optimal play gives W = max_T W_T.

    # Choices for Player 2: T tosses, success prob 2^-T, score 2^(T-1).
    choices = []
    t = 1
    while 2 ** (t - 1) < 2 * TARGET:
        choices.append((2 ** (t - 1), 1.0 / (2 ** t)))
        t += 1

    W = [[0.0] * (TARGET + 1) for _ in range(TARGET + 1)]

    for b in range(1, TARGET + 1):
        for a in range(1, TARGET + 1):
            # A = V(a-1, b): Player 1 scored; if a == 1, Player 1 has won.
            if a == 1:
                A = 0.0
            else:
                # Player 2 to move against W[a-1][...]; failure returns to
                # W[a-1][b], which is already computed (smaller a).
                Wa1b = W[a - 1][b]
                best = 0.0
                for s, p in choices:
                    w = 1.0 if s >= b else W[a - 1][b - s]
                    v = p * w + (1.0 - p) * Wa1b
                    if v > best:
                        best = v
                A = best

            # W[a][b] = max_T (A + p*w_T) / (1 + p) with self-loop solved.
            best = 0.0
            for s, p in choices:
                w = 1.0 if s >= b else W[a][b - s]
                v = (A + p * w) / (1.0 + p)
                if v > best:
                    best = v
            W[a][b] = best

    return f"{W[TARGET][TARGET]:.8f}"

if __name__ == "__main__":
    print(solve())
