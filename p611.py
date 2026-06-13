from math import isqrt


LIMIT = 10**12


def primes_up_to(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def chi4_prefix_without_one(n):
    # Sum of the non-principal character mod 4 over 2..n.
    return (1 if n & 3 in (1, 2) else 0) - 1


class PrimeCounterMod4:
    """Prime counts and prime character sums at Legendre quotient values."""

    def __init__(self, limit):
        self.limit = limit
        self.root = isqrt(limit)
        root = self.root

        small_pi = [0] * (root + 1)
        small_chi = [0] * (root + 1)
        large_pi = [0] * (root + 1)
        large_chi = [0] * (root + 1)

        for i in range(1, root + 1):
            small_pi[i] = i - 1
            small_chi[i] = chi4_prefix_without_one(i)
            quotient = limit // i
            large_pi[i] = quotient - 1
            large_chi[i] = chi4_prefix_without_one(quotient)

        for p in range(2, root + 1):
            if small_pi[p] == small_pi[p - 1]:
                continue

            pi_before = small_pi[p - 1]
            chi_before = small_chi[p - 1]
            chi_p = 0 if p == 2 else (1 if p & 3 == 1 else -1)
            square = p * p
            large_limit = min(root, limit // square)

            if chi_p:
                for i in range(1, large_limit + 1):
                    reduced = (limit // i) // p
                    if reduced <= root:
                        reduced_pi = small_pi[reduced]
                        reduced_chi = small_chi[reduced]
                    else:
                        index = limit // reduced
                        reduced_pi = large_pi[index]
                        reduced_chi = large_chi[index]
                    large_pi[i] -= reduced_pi - pi_before
                    large_chi[i] -= chi_p * (reduced_chi - chi_before)

                for value in range(root, square - 1, -1):
                    small_pi[value] -= small_pi[value // p] - pi_before
                    small_chi[value] -= chi_p * (small_chi[value // p] - chi_before)
            else:
                for i in range(1, large_limit + 1):
                    reduced = (limit // i) // p
                    reduced_pi = (
                        small_pi[reduced]
                        if reduced <= root
                        else large_pi[limit // reduced]
                    )
                    large_pi[i] -= reduced_pi - pi_before

                for value in range(root, square - 1, -1):
                    small_pi[value] -= small_pi[value // p] - pi_before

        self.small_pi = small_pi
        self.small_chi = small_chi
        self.large_pi = large_pi
        self.large_chi = large_chi

    def _counts(self, value):
        if value <= self.root:
            return self.small_pi[value], self.small_chi[value]
        index = self.limit // value
        return self.large_pi[index], self.large_chi[index]

    def pi_1_mod_4(self, value):
        if value < 5:
            return 0
        prime_count, character_sum = self._counts(value)
        return (prime_count - 1 + character_sum) // 2


def square_core_prefix(limit, primes):
    parity = bytearray(limit + 1)
    for p in primes:
        if p & 3 != 1:
            continue
        power = p
        while power <= limit:
            for multiple in range(power, limit + 1, power):
                parity[multiple] ^= 1
            if power > limit // p:
                break
            power *= p

    prefix = [0] * (limit + 1)
    running = 0
    for n in range(1, limit + 1):
        running += parity[n]
        prefix[n] = running
    return prefix


def prime_square_sum(limit, primes, counter):
    root = isqrt(limit)
    total = 0

    for p in primes:
        if p > root:
            break
        if p & 3 == 1:
            total += isqrt(limit // p)

    max_tail_weight = isqrt(limit // (root + 1))
    for weight in range(1, max_tail_weight + 1):
        high = limit // (weight * weight)
        low = limit // ((weight + 1) * (weight + 1)) + 1
        if low <= root:
            low = root + 1
        if low <= high:
            total += weight * (
                counter.pi_1_mod_4(high) - counter.pi_1_mod_4(low - 1)
            )

    return total


def embedded_prime_correction(limit, primes):
    total = 0
    for p in primes:
        if p & 3 != 1:
            continue
        power = p * p * p
        if power > limit:
            break
        fourth_power = p**4
        while power <= limit:
            choices = isqrt(limit // power)
            total += choices - choices // p
            if power > limit // fourth_power:
                break
            power *= fourth_power
    return total


def count_single_core(limit, primes, square_prefix, counter):
    square_or_twice_square = square_prefix[isqrt(limit)]
    single_prime_core = (
        prime_square_sum(limit, primes, counter)
        - embedded_prime_correction(limit, primes)
    )
    return square_or_twice_square + single_prime_core


def solve(limit=LIMIT):
    root = isqrt(limit)
    primes = primes_up_to(root)
    square_prefix = square_core_prefix(root, primes)

    counter = PrimeCounterMod4(limit)
    total = count_single_core(limit, primes, square_prefix, counter)

    half = limit // 2
    if limit == LIMIT:
        half_counter = counter
    else:
        half_counter = PrimeCounterMod4(half)
    total += count_single_core(half, primes, square_prefix, half_counter)
    return total


if __name__ == "__main__":
    print(solve())
