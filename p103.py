#!/usr/bin/env python3
def check_special(s):
    s = sorted(s)
    n = len(s)
    for k in range(1, n):
        if sum(s[:k+1]) <= sum(s[-(k):]):
            return False
    sums = set()
    for mask in range(1, 1 << n):
        total = sum(s[i] for i in range(n) if mask & (1 << i))
        if total in sums:
            return False
        sums.add(total)
    return True

def solve():
    # n=6 optimum: {11,18,19,20,22,25}
    # For n=7, search around "rule" candidate:
    # b ≈ 20 (middle of n=6 set)
    # candidate: {20+a, 31+a, 38+a, 39+a, 40+a, 42+a, 45+a}
    # Search with offsets around this
    
    n = 7
    best_sum = float('inf')
    best_str = ""
    
    # Search around closely - the optimum won't be far from the rule candidate
    # Using a DFS with tight bounds
    for a1 in range(18, 25):
        for a2 in range(a1 + 1, a1 + 15):
            if a1 + a2 <= a1 + 25: continue  # lower bound for a7
            for a3 in range(a2 + 1, a2 + 15):
                if sum([a1,a2,a3]) >= best_sum: break
                # a1+a2+a3 > a6+a7 => a7 < a1+a2+a3-a6, and a6 > a5
                for a4 in range(a3 + 1, a3 + 15):
                    if sum([a1,a2,a3,a4]) >= best_sum: break
                    for a5 in range(a4 + 1, a4 + 15):
                        if sum([a1,a2,a3,a4,a5]) >= best_sum: break
                        # a1+a2+a3+a4 > a5+a6+a7 => a7 < a1+a2+a3+a4-a5 - a6
                        for a6 in range(a5 + 1, a5 + 15):
                            if sum([a1,a2,a3,a4,a5,a6]) >= best_sum: break
                            max_a7 = a1 + a2 - 1
                            if max_a7 <= a6: continue
                            min_a7 = a6 + 1
                            for a7 in range(min_a7, min(max_a7 + 1, a6 + 10)):
                                s = [a1,a2,a3,a4,a5,a6,a7]
                                if sum(s) >= best_sum: continue
                                ok = True
                                for k in range(1, n):
                                    if sum(s[:k+1]) <= sum(s[-(k):]):
                                        ok = False; break
                                if not ok: continue
                                if check_special(s):
                                    best_sum = sum(s)
                                    best_str = "".join(str(x) for x in s)
    return best_str

if __name__ == "__main__":
    print(solve())
