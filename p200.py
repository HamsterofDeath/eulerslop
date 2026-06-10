def solve():
    limit = 600000
    is_prime = [True] * limit
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit, i):
                is_prime[j] = False
    primes = [i for i, p in enumerate(is_prime) if p]
    
    LIMIT = 3 * 10**11
    
    def is_prime_mr(n):
        if n < 2:
            return False
        if n in (2, 3, 5, 7):
            return True
        if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
            return False
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            if a >= n:
                break
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def is_prime_proof(n):
        s = str(n)
        last_digit_even = s[-1] in '024568'
        
        if last_digit_even:
            prefix = s[:-1]
            orig_last = s[-1]
            for d in '0123456789':
                if d == orig_last:
                    continue
                val = int(prefix + d)
                if is_prime_mr(val):
                    return False
            return True
        else:
            for i in range(len(s)):
                orig = s[i]
                for d in '0123456789':
                    if d == orig:
                        continue
                    if i == 0 and d == '0':
                        continue
                    val = int(s[:i] + d + s[i+1:])
                    if is_prime_mr(val):
                        return False
            return True

    candidates = []
    max_q = int((LIMIT / 4) ** (1/3)) + 1
    
    for q in primes:
        if q > max_q:
            break
        q3 = q ** 3
        max_p = int((LIMIT / q3) ** 0.5) + 1
        for p in primes:
            if p > max_p:
                break
            if p == q:
                continue
            val = p * p * q3
            if val >= LIMIT:
                continue
            if "200" in str(val):
                candidates.append(val)
                
    candidates.sort()
    
    count = 0
    for val in candidates:
        if is_prime_proof(val):
            count += 1
            if count == 200:
                print(val)
                break

if __name__ == "__main__":
    solve()
