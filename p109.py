#!/usr/bin/env python3

def solve():
    # All possible darts as (score, type) - type is for identity
    # S1-S20, S25
    singles = [(s, "S"+str(s)) for s in range(1, 21)] + [(25, "S25")]
    # D1-D20, D25
    doubles = [(2*s, "D"+str(s)) for s in range(1, 21)] + [(50, "D25")]
    # T1-T20
    trebles = [(3*s, "T"+str(s)) for s in range(1, 21)]
    
    all_darts = singles + doubles + trebles  # 62 total
    
    # Checkout doubles (final dart must be a double)
    checkout_doubles = [(2*s, "D"+str(s)) for s in range(1, 21)] + [(50, "D25")]
    
    limit = 100
    count = 0
    
    # 1 dart checkout
    for score, ident in checkout_doubles:
        if score < limit:
            count += 1
    
    # 2 dart checkout: first dart (any) + checkout double
    for c_score, c_ident in checkout_doubles:
        remaining = limit - c_score - 1
        for s_score, s_ident in all_darts:
            if 0 < s_score <= remaining:
                count += 1
    
    # 3 dart checkout: two non-checkout darts + checkout double
    # Non-checkout darts are unordered among themselves
    # So we count each unordered pair once
    for c_score, c_ident in checkout_doubles:
        max_sum = limit - c_score - 1
        seen_pairs = set()
        for i, (s1, id1) in enumerate(all_darts):
            if s1 > max_sum:
                continue
            for j, (s2, id2) in enumerate(all_darts):
                if s1 + s2 > max_sum:
                    continue
                # Canonical ordering for the unordered pair
                if i <= j:
                    pair = (i, j)
                else:
                    pair = (j, i)
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    count += 1
    
    return count

if __name__ == "__main__":
    print(solve())
