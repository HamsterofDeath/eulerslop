#!/usr/bin/env python3
"""p189: Tri-colouring a triangular grid

Count the number of valid 3-colourings of a triangular grid of height 8.
Uses row-by-row DP with a recursive DFS transition to prune invalid states.
"""

def solve():
    H = 8
    # choices[u1][u2][u3] is the number of valid colors for a downwards triangle
    # adjacent to upwards triangles with colors u1, u2, u3
    choices = [[[3 - len({u1, u2, u3}) for u3 in range(3)] for u2 in range(3)] for u1 in range(3)]
    
    # dp is a dict mapping state (tuple of length r) to count of valid colorings
    dp = {(0,): 1, (1,): 1, (2,): 1}
    
    for r in range(2, H + 1):
        prev_len = r - 1
        curr_len = r
        next_dp = {}
        
        # Temp buffer to build current row's tuple
        current_tuple = [0] * curr_len
        
        def dfs(j, u_prev, ways, multiplier):
            if multiplier == 0:
                return
            if j == curr_len:
                tup = tuple(current_tuple)
                next_dp[tup] = next_dp.get(tup, 0) + ways * multiplier
                return
                
            for val in range(3):
                current_tuple[j] = val
                if j == 0:
                    dfs(1, u_prev, ways, multiplier)
                else:
                    c = choices[current_tuple[j-1]][val][u_prev[j-1]]
                    dfs(j + 1, u_prev, ways, multiplier * c)
                    
        for u_prev, ways in dp.items():
            dfs(0, u_prev, ways, 1)
            
        dp = next_dp
        
    return sum(dp.values())

if __name__ == "__main__":
    print(solve())
