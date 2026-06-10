#!/usr/bin/env python3
"""p161: Tiling 9x12 grid with triominoes. DP with column profile."""
def solve():
    H = 9
    W = 12
    
    shapes = [
        [(0,0),(1,0),(2,0)],           # vertical 3x1
        [(0,0),(0,1),(0,2)],           # horizontal 1x3
        [(0,0),(0,1),(1,0)],           # L missing BR
        [(0,0),(1,0),(1,1)],           # L missing TR
        [(0,0),(0,1),(1,1)],           # L missing BL
        [(0,0),(-1,1),(0,1)],          # L missing TL (anchor at bottom-left)
    ]
    
    # Precompute for each shape: which columns are modified
    # We'll check validity at placement time.
    
    states = 1 << H
    
    # DP: dp[col][cur][nxt][nx2] = number of ways
    # cur: filled cells in current column (from previous placements)
    # nxt: filled cells in next column (claimed by shapes starting in previous columns)
    # nx2: filled cells in column+2 (claimed by horizontal shapes)
    
    memo = {}
    def dp(col, cur, nxt, nx2):
        if col == W:
            return 1 if cur == 0 and nxt == 0 and nx2 == 0 else 0
        
        key = (col, cur, nxt, nx2)
        if key in memo:
            return memo[key]
        
        # Find first unfilled cell in current column (cur has 1 = filled)
        # We need to fill cells where cur has 0.
        r = 0
        while r < H and (cur & (1 << r)):
            r += 1
        
        if r == H:
            # All cells in current column filled, move to next column
            res = dp(col + 1, nxt, nx2, 0)
            memo[key] = res
            return res
        
        total = 0
        
        for shape in shapes:
            ok = True
            new_cur = cur
            new_nxt = nxt
            new_nx2 = nx2
            
            for dr, dc in shape:
                rr = r + dr
                cc = col + dc
                
                if rr < 0 or rr >= H or cc < col or cc >= W:
                    ok = False
                    break
                
                if cc == col:
                    if new_cur & (1 << rr):
                        ok = False
                        break
                    new_cur |= (1 << rr)
                elif cc == col + 1:
                    if new_nxt & (1 << rr):
                        ok = False
                        break
                    new_nxt |= (1 << rr)
                elif cc == col + 2:
                    if new_nx2 & (1 << rr):
                        ok = False
                        break
                    new_nx2 |= (1 << rr)
                else:
                    ok = False
                    break
            
            if ok:
                total += dp(col, new_cur, new_nxt, new_nx2)
        
        memo[key] = total
        return total
    
    return dp(0, 0, 0, 0)

if __name__ == "__main__":
    print(solve())
