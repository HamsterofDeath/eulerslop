def solve():
    N = 30
    dp = [[0] * 3 for _ in range(2)]
    dp[0][0] = 1
    
    for day in range(N):
        next_dp = [[0] * 3 for _ in range(2)]
        for l in range(2):
            for a in range(3):
                ways = dp[l][a]
                if ways == 0:
                    continue
                next_dp[l][0] += ways
                if a + 1 < 3:
                    next_dp[l][a + 1] += ways
                if l + 1 < 2:
                    next_dp[l + 1][0] += ways
        dp = next_dp
        
    total_30 = sum(dp[l][a] for l in range(2) for a in range(3))
    print(total_30)

if __name__ == "__main__":
    solve()
