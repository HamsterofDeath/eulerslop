import math

MOD = 10**8

def SA(c: int) -> int:
    return c**5 - 9 * c**4 + 34 * c**3 - 69 * c**2 + 77 * c - 38

def SB(c: int) -> int:
    return c**5 - 8 * c**4 + 27 * c**3 - 50 * c**2 + 52 * c - 24

def solve():
    a = 25
    b = 75
    c = 1984
    
    n = a + b
    comb = math.comb(n, a)
    
    # We can do modular arithmetic for each part to avoid huge numbers,
    # or just let Python handle large integers and take % MOD.
    # Evaluating SA(c) and SB(c) modulo MOD:
    sa = SA(c) % MOD
    sb = SB(c) % MOD
    
    ans = (comb % MOD) * (c % MOD) % MOD
    ans = ans * ((c - 1) % MOD) % MOD
    ans = ans * pow(sa, a, MOD) % MOD
    ans = ans * pow(sb, b, MOD) % MOD
    
    # We want the last 8 digits.
    # Format with leading zeros if necessary to make it 8 digits?
    # The problem asks for "the last 8 digits of N(25,75,1984)".
    # If the number is smaller than 10^7, we might need leading zeros.
    # Let's print both raw and formatted to see.
    print(ans)

if __name__ == "__main__":
    solve()
