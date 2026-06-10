#!/usr/bin/env python3
"""p151: Expected number of times a single sheet is found in envelope (batches 2-15).
State: (a2,a3,a4,a5). Initial state after batch 1: (1,1,1,1).
Transitions: pick random sheet. A5: use it. Larger: cut until A5, return rest."""
from functools import lru_cache

def solve():
    @lru_cache(maxsize=None)
    def dp(a2, a3, a4, a5, batches_left):
        # batches_left: number of remaining batches INCLUDING current
        if batches_left == 0:
            return (0.0, 0.0)  # (expected singles, total probability)
        total = a2 + a3 + a4 + a5
        if total == 0:
            return (0.0, 0.0)
        
        exp_singles = 0.0
        # Record if this batch finds single sheet (exclude the last batch of the week)
        is_single = 1.0 if total == 1 and batches_left > 1 else 0.0
        
        # Pick A5
        if a5 > 0:
            prob = a5 / total
            sub_exp, _ = dp(a2, a3, a4, a5 - 1, batches_left - 1)
            exp_singles += prob * (is_single + sub_exp)
        
        # Pick A4 -> cut to A5: use one, return one A5
        if a4 > 0:
            prob = a4 / total
            sub_exp, _ = dp(a2, a3, a4 - 1, a5 + 1, batches_left - 1)
            exp_singles += prob * (is_single + sub_exp)
        
        # Pick A3 -> cut: return one A4, cut other A4 -> use A5, return A5
        if a3 > 0:
            prob = a3 / total
            sub_exp, _ = dp(a2, a3 - 1, a4 + 1, a5 + 1, batches_left - 1)
            exp_singles += prob * (is_single + sub_exp)
        
        # Pick A2 -> cut: return A3, A4, A5
        if a2 > 0:
            prob = a2 / total
            sub_exp, _ = dp(a2 - 1, a3 + 1, a4 + 1, a5 + 1, batches_left - 1)
            exp_singles += prob * (is_single + sub_exp)
        
        return (exp_singles, 1.0)
    
    # Batch 1 already done. State: (1,1,1,1). 15 batches remaining.
    result, _ = dp(1, 1, 1, 1, 15)
    return f"{result:.6f}"

if __name__ == "__main__":
    print(solve())
