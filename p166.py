#!/usr/bin/env python3
"""p166: 4x4 grid of digits 0-9 with equal row/col/diag sums. Optimized enumeration."""
def solve():
    total = 0
    for S in range(37):
        # Precompute all possible rows
        rows = []
        for a in range(10):
            for b in range(10):
                for c in range(10):
                    d = S - a - b - c
                    if 0 <= d <= 9:
                        rows.append((a, b, c, d))
        
        for a, b, c, d in rows:
            for e, f, g, h in rows:
                # Anti-diag: d + g + j + m = S → m = S - d - g - j
                # Col1: a + e + i + m = S → i = S - a - e - m
                # Substitute m: i = S - a - e - (S - d - g - j) = d + g + j - a - e
                # So: j = i + a + e - d - g
                
                for i in range(10):
                    m = S - a - e - i
                    if not (0 <= m <= 9):
                        continue
                    
                    j = a + e + i - d - g  # from anti-diag consistency
                    if not (0 <= j <= 9):
                        continue
                    
                    # Verify col2: n = S - b - f - j
                    n = S - b - f - j
                    if not (0 <= n <= 9):
                        continue
                    
                    # From diagonal and row3: find k, l
                    # Main diag: a + f + k + p = S → p = S - a - f - k
                    # Col4: d + h + l + p = S → p = S - d - h - l
                    # Equating: S - a - f - k = S - d - h - l → k - l = d + h - a - f
                    # Row3: i + j + k + l = S → k + l = S - i - j
                    # Solving: k = (S - i - j + d + h - a - f) / 2
                    #          l = (S - i - j - d - h + a + f) / 2
                    
                    num_k = S - i - j + d + h - a - f
                    num_l = S - i - j - d - h + a + f
                    
                    if num_k & 1 or num_l & 1:
                        continue
                    
                    k = num_k // 2
                    l = num_l // 2
                    
                    if not (0 <= k <= 9 and 0 <= l <= 9):
                        continue
                    
                    # Compute o, p
                    o = S - c - g - k
                    if not (0 <= o <= 9):
                        continue
                    p = S - d - h - l
                    if not (0 <= p <= 9):
                        continue
                    
                    # Verify row4: m + n + o + p = S
                    if m + n + o + p != S:
                        continue
                    
                    # Verify main diag: a + f + k + p = S
                    if a + f + k + p != S:
                        continue
                    
                    # Verify col3: c + g + k + o = S (should be true by o definition)
                    if c + g + k + o != S:
                        continue
                    
                    total += 1
    
    return total

if __name__ == "__main__":
    print(solve())
