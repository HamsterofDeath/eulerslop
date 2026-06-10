import math

def solve():
    MAX_VAL = 4000000
    is_sq = [False] * MAX_VAL
    for i in range(int(math.isqrt(MAX_VAL - 1)) + 1):
        is_sq[i * i] = True
        
    for a in range(1, 2000):
        a2 = a * a
        for b in range(a - 2, 0, -2):
            b2 = b * b
            x = (a2 + b2) // 2
            y = (a2 - b2) // 2
            
            c_min = math.isqrt(y) + 1
            c_max = math.isqrt(2 * y - 1)
            
            for c in range(c_min, c_max + 1):
                c2 = c * c
                z = c2 - y
                
                if is_sq[y - z] and is_sq[x - z] and is_sq[x + z]:
                    return x + y + z

def main():
    print(solve())

if __name__ == "__main__":
    main()
