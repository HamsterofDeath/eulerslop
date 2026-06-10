#!/usr/bin/env python3
"""p185: Number Mind

Find the unique 16-digit secret sequence from 22 guesses and their match counts.
This is formulated as a Mixed-Integer Linear Program (MILP) and solved via SciPy.
"""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def solve():
    guesses = [
        ("5616185650518293", 2),
        ("3847439647293047", 1),
        ("5855462940810587", 3),
        ("9742855507068353", 3),
        ("4296849643607543", 3),
        ("3174248439465858", 1),
        ("4513559094146117", 2),
        ("7890971548908067", 3),
        ("8157356344118483", 1),
        ("2615250744386899", 2),
        ("8690095851526254", 3),
        ("6375711915077050", 1),
        ("6913859173121360", 1),
        ("6442889055042768", 2),
        ("2321386104303845", 0),
        ("2326509471271448", 2),
        ("5251583379644322", 2),
        ("1748270476758276", 3),
        ("4895722652190306", 1),
        ("3041631117224635", 3),
        ("1841236454324589", 3),
        ("2659862637316867", 2),
    ]
    
    num_vars = 160
    
    A = []
    lb = []
    ub = []
    
    # 1. One digit per position: sum_{d=0..9} x[p * 10 + d] = 1
    for p in range(16):
        row = np.zeros(num_vars)
        for d in range(10):
            row[p * 10 + d] = 1
        A.append(row)
        lb.append(1)
        ub.append(1)
        
    # 2. Guess matching constraints: sum_{p=0..15} x[p * 10 + digit] = target
    for guess, target in guesses:
        row = np.zeros(num_vars)
        for p in range(16):
            digit = int(guess[p])
            row[p * 10 + digit] = 1
        A.append(row)
        lb.append(target)
        ub.append(target)
        
    A = np.array(A)
    lb = np.array(lb)
    ub = np.array(ub)
    
    c = np.zeros(num_vars)
    bounds = Bounds(np.zeros(num_vars), np.ones(num_vars))
    integrality = np.ones(num_vars)
    
    constraint = LinearConstraint(A, lb, ub)
    res = milp(c=c, bounds=bounds, constraints=constraint, integrality=integrality)
    
    if res.success:
        x = np.round(res.x).astype(int)
        solution = []
        for p in range(16):
            for d in range(10):
                if x[p * 10 + d] == 1:
                    solution.append(d)
                    break
        return "".join(map(str, solution))
    else:
        return None

if __name__ == "__main__":
    print(solve())
