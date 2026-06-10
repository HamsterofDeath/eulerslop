#!/usr/bin/env python3
"""p182: RSA encryption

Find the sum of all values of e, 1 < e < phi(p,q) and gcd(e, phi) = 1,
so that the number of unconcealed messages is minimized.
Unconcealed messages m satisfy m^e = m mod n.
The number of such messages is (1 + gcd(e-1, p-1)) * (1 + gcd(e-1, q-1)).
"""
import math

def solve():
    p = 1009
    q = 3643
    phi = (p - 1) * (q - 1)
    
    # The number of unconcealed messages is (1 + gcd(e-1, p-1)) * (1 + gcd(e-1, q-1)).
    # Since e is coprime to phi, e must be odd.
    # Thus e-1 is even, so gcd(e-1, p-1) >= 2 and gcd(e-1, q-1) >= 2.
    # The minimum possible value of the product is (1 + 2) * (1 + 2) = 9.
    # This minimum is achieved when gcd(e-1, p-1) == 2 and gcd(e-1, q-1) == 2.
    
    ans_sum = 0
    p_minus_1 = p - 1
    q_minus_1 = q - 1
    
    for e in range(2, phi):
        if math.gcd(e, phi) == 1:
            if math.gcd(e - 1, p_minus_1) == 2 and math.gcd(e - 1, q_minus_1) == 2:
                ans_sum += e
                
    return ans_sum

if __name__ == "__main__":
    print(solve())
