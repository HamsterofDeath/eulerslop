#!/usr/bin/env python3
import numpy as np


def count_sets(n):
    # A die is a multiset of 6 faces from 1..n.  Rolling X against Y, the
    # second player wins with probability W(X,Y)/36 where
    # W(X,Y) = #{(x,y) : x > y}; ties count for neither player, so
    # "X beats Y" (win chance > 1/2) means W(X,Y) > 18, which is strictly
    # stronger than W(X,Y) > W(Y,X).
    # A set of three dice is nontransitive iff every die is beaten by some
    # other die in the set; W(X,Y) + W(Y,X) <= 36 means each pair beats in
    # at most one direction, so with three pairs every in-degree must be
    # exactly 1: a directed 3-cycle A->B->C->A.  Each unordered set yields
    # exactly its 3 cyclic rotations as ordered cycles (reversals fail), so
    #   answer = #{ordered (A,B,C) : W(A,B)>18, W(B,C)>18, W(C,A)>18} / 3.
    #
    # Count ordered triples by sweeping the face value v = 1..n and deciding
    # how many faces of value v each die gets.  DP state: (al, be, ga) =
    # faces placed so far on A, B, C, plus the partial win counts
    #   w1 = W(A,B), w2 = W(B,C), w3 = W(C,A)
    # over the faces placed so far.  Adding (a, b, c) faces of value v
    # (all previously placed faces are strictly smaller, equal values tie):
    #   w1 += a*be,  w2 += b*ga,  w3 += c*al.
    # Since 0 <= w1 <= al*be (etc.), each (al,be,ga) bucket stores a dense
    # int64 cube of exactly the reachable w-range; transitions are numpy
    # shifted slice-adds.  Final counts fit in int64: C(n+5,6)^3 < 2^63.
    states = {(0, 0, 0): np.ones((1, 1, 1), dtype=np.int64)}
    for _ in range(n):
        new = {}
        for (al, be, ga), arr in states.items():
            m1, m2, m3 = al * be + 1, be * ga + 1, ga * al + 1
            for a in range(7 - al):
                na = al + a
                for b in range(7 - be):
                    nb = be + b
                    s1 = a * be
                    for c in range(7 - ga):
                        nc = ga + c
                        key = (na, nb, nc)
                        s2, s3 = b * ga, c * al
                        tgt = new.get(key)
                        if tgt is None:
                            tgt = np.zeros((na * nb + 1, nb * nc + 1,
                                            nc * na + 1), dtype=np.int64)
                            new[key] = tgt
                        tgt[s1:s1 + m1, s2:s2 + m2, s3:s3 + m3] += arr
        states = new
    final = states[(6, 6, 6)]  # w-axes span 0..36
    cyclic = int(final[19:, 19:, 19:].sum())  # each win count > 18
    return cyclic // 3


def solve():
    assert count_sets(7) == 9780  # value given in the problem statement
    return count_sets(30)


if __name__ == "__main__":
    print(solve())
