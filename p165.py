#!/usr/bin/env python3
import numpy as np

def solve():
    # Generate Blum Blum Shub
    s = 290797
    M = 50515093
    t = []
    for _ in range(20000):
        s = (s * s) % M
        t.append(s % 500)
        
    t = np.array(t, dtype=np.int32)
    X1 = t[0::4]
    Y1 = t[1::4]
    X2 = t[2::4]
    Y2 = t[3::4]
    
    DX = X2 - X1
    DY = Y2 - Y1
    
    # D[i, j] = DX(j) DY(i) - DX(i) DY(j)
    D = DX[None, :] * DY[:, None] - DX[:, None] * DY[None, :]
    
    Y_diff = Y1[None, :] - Y1[:, None]
    X_diff = X1[None, :] - X1[:, None]
    
    N1 = DX[None, :] * Y_diff - DY[None, :] * X_diff
    N2 = DX[:, None] * Y_diff - DY[:, None] * X_diff
    
    cond_pos = (D > 0) & (N1 > 0) & (N1 < D) & (N2 > 0) & (N2 < D)
    cond_neg = (D < 0) & (N1 < 0) & (N1 > D) & (N2 < 0) & (N2 > D)
    
    valid = cond_pos | cond_neg
    
    # Keep only i < j
    upper_tri = np.triu(np.ones_like(D, dtype=bool), k=1)
    valid &= upper_tri
    
    I, J = np.where(valid)
    
    # Extract values for valid intersections
    val_D = D[I, J]
    val_N1 = N1[I, J]
    
    val_X1 = X1[I]
    val_Y1 = Y1[I]
    val_DX1 = DX[I]
    val_DY1 = DY[I]
    
    num_x = val_X1.astype(np.int64) * val_D + val_N1 * val_DX1
    num_y = val_Y1.astype(np.int64) * val_D + val_N1 * val_DY1
    val_D_64 = val_D.astype(np.int64)
    
    g_x = np.gcd(num_x, val_D_64)
    px_num = num_x // g_x
    px_den = val_D_64 // g_x
    mask_x = px_den < 0
    px_num[mask_x] = -px_num[mask_x]
    px_den[mask_x] = -px_den[mask_x]
    
    g_y = np.gcd(num_y, val_D_64)
    py_num = num_y // g_y
    py_den = val_D_64 // g_y
    mask_y = py_den < 0
    py_num[mask_y] = -py_num[mask_y]
    py_den[mask_y] = -py_den[mask_y]
    
    points = set(zip(zip(px_num, px_den), zip(py_num, py_den)))
    print(len(points))

if __name__ == "__main__":
    solve()
