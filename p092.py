#!/usr/bin/env python3

def solve():
    # DP table: dp[i][s] is the number of ways to have sum of squares = s with i digits
    # i goes up to 7 (for numbers up to 9,999,999)
    max_sum = 7 * 81
    dp = [0] * (max_sum + 1)
    dp[0] = 1
    
    for _ in range(7):
        next_dp = [0] * (max_sum + 1)
        for s in range(max_sum + 1):
            if dp[s] > 0:
                for d in range(10):
                    ns = s + d*d
                    if ns <= max_sum:
                        next_dp[ns] += dp[s]
        dp = next_dp
        
    memo = {1: 1, 89: 89}
    def leads_to_89(n):
        if n == 0:
            return False
        chain = []
        cur = n
        while cur not in memo:
            chain.append(cur)
            cur = sum(int(d)**2 for d in str(cur))
        end = memo[cur]
        for x in chain:
            memo[x] = end
        return end == 89

    ans = 0
    for s in range(1, max_sum + 1):
        if leads_to_89(s):
            ans += dp[s]
            
    return ans

if __name__ == "__main__":
    print(solve())
