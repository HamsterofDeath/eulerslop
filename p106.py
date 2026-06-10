#!/usr/bin/env python3
from itertools import combinations
from math import comb

def solve():
    n = 12
    # We assume rule 2 holds. Rule 1 only needs testing for pairs of disjoint
    # subsets of EQUAL size (since rule 2 handles unequal sizes).
    # Also, if B and C are disjoint and |B|=|C|, we need to test whether S(B)=S(C).
    # But some pairs are guaranteed different by rule 2:
    # If we can pair elements of B and C such that each element of B is less
    # than the corresponding element of C, then S(B) < S(C) without testing.
    # We only need to test pairs where this pairing doesn't hold.
    #
    # For given subsets B,C with |B|=|C|=k, sort them b1<b2<...<bk, c1<c2<...<ck.
    # If bi < ci for all i, then S(B) < S(C) by rule 2 (already satisfied).
    # If ci < bi for all i, then S(C) < S(B).
    # We only need to test when the sorted elements interleave.
    
    count = 0
    elements = list(range(n))
    
    for k in range(1, n // 2 + 1):
        for b_indices in combinations(elements, k):
            remaining = [i for i in range(n) if i not in b_indices]
            for c_indices in combinations(remaining, k):
                # Ensure B is the one with smaller first element for canonical ordering
                if b_indices[0] < c_indices[0]:
                    pass  # B is properly first
                elif b_indices[0] > c_indices[0]:
                    continue  # swap would make it the same pair
                else:
                    # First elements can't be equal since disjoint
                    pass
                
                # Check if the interleaving requires testing
                b = list(b_indices)
                c = list(c_indices)
                needs_test = False
                for i in range(k):
                    if b[i] > c[i]:
                        needs_test = True
                        break
                if not needs_test:
                    # All b_i < c_i, S(B) < S(C) guaranteed
                    continue
                needs_test = False
                for i in range(k):
                    if c[i] > b[i]:
                        needs_test = True
                        break
                if not needs_test:
                    # All c_i < b_i, S(C) < S(B) guaranteed
                    continue
                count += 1
    
    return count

if __name__ == "__main__":
    print(solve())
