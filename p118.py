#!/usr/bin/env python3
from itertools import permutations, combinations
from math import isqrt

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    limit = isqrt(n)
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def solve():
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    primes_for_mask = [[] for _ in range(512)]
    
    for k in range(1, 10):
        for comb in combinations(digits, k):
            # If sum(comb) % 3 == 0 and k > 1, all permutations are divisible by 3 (composite)
            if k > 1 and sum(comb) % 3 == 0:
                continue
                
            mask = 0
            for d in comb:
                mask |= (1 << (d - 1))
            
            seen_nums = []
            
            if k == 1:
                num = comb[0]
                if num in {2, 3, 5, 7}:
                    seen_nums.append(num)
            else:
                valid_lasts = [d for d in comb if d in {1, 3, 7, 9}]
                for last in valid_lasts:
                    rem = [d for d in comb if d != last]
                    for perm in permutations(rem):
                        num = 0
                        for d in perm:
                            num = num * 10 + d
                        num = num * 10 + last
                        seen_nums.append(num)
                        
            for num in seen_nums:
                if is_prime(num):
                    primes_for_mask[mask].append(num)
                    
            primes_for_mask[mask].sort()
            
    memo = {}

    def count_partitions(mask):
        if mask == 0:
            return 1

        if mask in memo:
            return memo[mask]

        # Canonical enumeration: the block containing the lowest unused digit
        # uniquely identifies each partition, so just multiply by the number
        # of primes available for that block.
        first_bit = (mask & -mask).bit_length() - 1
        ans = 0

        submask = mask
        while submask > 0:
            if (submask & (1 << first_bit)):
                ans += len(primes_for_mask[submask]) * count_partitions(mask ^ submask)

            submask = (submask - 1) & mask

        memo[mask] = ans
        return ans

    return count_partitions(511)

if __name__ == "__main__":
    print(solve())
