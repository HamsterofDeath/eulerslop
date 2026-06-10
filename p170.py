#!/usr/bin/env python3
from itertools import permutations
from math import gcd

def solve():
    # Precompute partitions of a 10-digit string
    partitions = []
    for mask in range(1, 512):
        cuts = []
        for i in range(9):
            if (mask >> i) & 1:
                cuts.append(i + 1)
        partitions.append(cuts)
        
    digits = set('0123456789')
    
    # Search pandigital numbers in descending order
    for perm in permutations('9876543210'):
        P_str = ''.join(perm)
        
        # Precompute substring integer values and check for leading zeros
        sub_int = [[0]*11 for _ in range(10)]
        has_leading_zero = [[False]*11 for _ in range(10)]
        for i in range(10):
            for j in range(i + 1, 11):
                sub_int[i][j] = int(P_str[i:j])
                has_leading_zero[i][j] = (P_str[i] == '0')
                
        # Check all partitions
        for cuts in partitions:
            invalid = False
            prev = 0
            g = None
            parts = []
            
            for c in cuts:
                if has_leading_zero[prev][c]:
                    invalid = True
                    break
                val = sub_int[prev][c]
                parts.append(val)
                if g is None:
                    g = val
                else:
                    g = gcd(g, val)
                    if g == 1:
                        invalid = True
                        break
                prev = c
                
            if invalid:
                continue
                
            if has_leading_zero[prev][10]:
                continue
            last_val = sub_int[prev][10]
            g = gcd(g, last_val)
            if g == 1:
                continue
                
            parts.append(last_val)
                
            # Find divisors of g
            divisors = []
            d = 2
            while d * d <= g:
                if g % d == 0:
                    divisors.append(d)
                    if d * d != g:
                        divisors.append(g // d)
                d += 1
            if g > 1 and g not in divisors:
                divisors.append(g)
                
            for X in divisors:
                concat = str(X) + ''.join(str(p // X) for p in parts)
                if len(concat) == 10 and set(concat) == digits:
                    return P_str

if __name__ == "__main__":
    print(solve())
