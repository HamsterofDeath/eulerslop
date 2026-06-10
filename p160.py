#!/usr/bin/env python3
"""p160: Last 5 digits before trailing zeros of (10^12)!.
Compute N! / 10^v5 mod 10^5, then use CRT (mod 32, mod 3125).
f(N) ≡ 0 mod 32 (since v2-v5 >> 5).
For mod 3125: compute X = N! / 5^v5 mod 3125, then f(N) = X * inv2^v5 mod 3125."""
def v_p(n, p):
    """Exponent of p in n!"""
    s = 0
    while n:
        n //= p
        s += n
    return s

def mod_pow(a, e, m):
    r = 1
    while e:
        if e & 1:
            r = (r * a) % m
        a = (a * a) % m
        e >>= 1
    return r

def solve():
    N = 10 ** 12
    M = 3125  # 5^5
    
    v5 = v_p(N, 5)
    v2 = v_p(N, 2)
    
    # Compute X = N! / 5^v5 mod M
    # G(N) = product of numbers 1..N with 5s removed, mod M.
    # G(N) = G(N//5) * H(N) where H(N) = product of i ≤ N, i not divisible by 5.
    
    def H(n):
        """Product of numbers 1..n not divisible by 5, mod M."""
        if n <= 0:
            return 1
        # Product over complete blocks of size M
        blocks = n // M
        rem = n % M
        
        # Product of all numbers 1..M not divisible by 5
        full = 1
        for i in range(1, M + 1):
            if i % 5 != 0:
                full = (full * i) % M
        res = mod_pow(full, blocks, M)
        
        for i in range(1, rem + 1):
            if i % 5 != 0:
                res = (res * i) % M
        return res
    
    def G(n):
        if n <= 0:
            return 1
        return (H(n) * G(n // 5)) % M
    
    X = G(N) % M
    
    # f(N) = X * (inv2)^v5 mod M
    inv2 = (M + 1) // 2  # inverse of 2 mod 3125 (since 2*1563 = 3126 ≡ 1)
    f_mod_3125 = (X * mod_pow(inv2, v5, M)) % M
    
    # f(N) mod 32 = 0
    f_mod_32 = 0
    
    # CRT: find y s.t. y ≡ 0 (mod 32), y ≡ f_mod_3125 (mod 3125)
    # y = f_mod_3125 + 3125 * t where t ≡ (0 - f_mod_3125) * inv(3125, 32) (mod 32)
    inv_3125_mod_32 = mod_pow(3125 % 32, 16 - 1, 32)  # Euler phi(32)=16, so inverse = a^(phi-1) mod 32
    # Actually 3125 % 32 = 3125 - 32*97 = 3125 - 3104 = 21
    # inv(21, 32): 21 * x ≡ 1 (mod 32)
    # 21*21=441=13*32+25... 21*29=609=19*32+1 → x=29
    inv_3125_mod_32 = 29
    
    t = ((0 - f_mod_3125) % 32) * inv_3125_mod_32 % 32
    y = f_mod_3125 + 3125 * t
    y %= 100000
    
    return y

if __name__ == "__main__":
    print(solve())
