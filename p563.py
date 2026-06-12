#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

using u64 = unsigned long long;
using u128 = __uint128_t;

static const int PRIME_COUNT = 9;
static const int PRIMES[PRIME_COUNT] = {2, 3, 5, 7, 11, 13, 17, 19, 23};
static const u64 LIMIT = 2300000000000000ULL;

struct SmoothNumber {
    u64 value;
    array<unsigned char, PRIME_COUNT> exponents;
};

vector<SmoothNumber> smooth_numbers;

void generate_smooth(int index, u64 value, array<unsigned char, PRIME_COUNT>& exponents) {
    if (index == PRIME_COUNT) {
        smooth_numbers.push_back({value, exponents});
        return;
    }

    u64 current = value;
    int exponent = 0;
    while (current <= LIMIT) {
        exponents[index] = exponent;
        generate_smooth(index + 1, current, exponents);
        if (current > LIMIT / PRIMES[index]) break;
        current *= PRIMES[index];
        ++exponent;
    }
    exponents[index] = 0;
}

u64 isqrt_u64(u64 n) {
    u64 r = sqrt((long double)n);
    while ((u128)(r + 1) * (r + 1) <= n) ++r;
    while ((u128)r * r > n) --r;
    return r;
}

int variant_count(const SmoothNumber& number) {
    u64 area = number.value;
    u64 high = isqrt_u64(area);

    // Count divisors d with area/d <= 11d/10, i.e. d^2 >= 10*area/11.
    u64 low = isqrt_u64((u64)((u128)10 * area / 11));
    while ((u128)low * low * 11 < (u128)10 * area) ++low;

    int count = 0;
    function<void(int, u64)> search = [&](int index, u64 divisor) {
        if (index == PRIME_COUNT) {
            if (low <= divisor && divisor <= high) ++count;
            return;
        }

        u64 current = divisor;
        for (int e = 0; e <= number.exponents[index]; ++e) {
            if (current <= high) search(index + 1, current);
            if (e == number.exponents[index]) break;
            if (current > high / PRIMES[index]) break;
            current *= PRIMES[index];
        }
    };
    search(0, 1);
    return count;
}

string to_string128(u128 value) {
    if (value == 0) return "0";
    string text;
    while (value > 0) {
        text.push_back(char('0' + value % 10));
        value /= 10;
    }
    reverse(text.begin(), text.end());
    return text;
}

int main() {
    array<unsigned char, PRIME_COUNT> exponents{};
    generate_smooth(0, 1, exponents);
    sort(smooth_numbers.begin(), smooth_numbers.end(), [](const SmoothNumber& a, const SmoothNumber& b) {
        return a.value < b.value;
    });

    vector<u64> minimal(101, 0);
    int found = 0;
    for (const SmoothNumber& number : smooth_numbers) {
        int variants = variant_count(number);
        if (2 <= variants && variants <= 100 && minimal[variants] == 0) {
            minimal[variants] = number.value;
            ++found;
            if (found == 99) break;
        }
    }

    if (minimal[3] != 889200ULL) return 1;
    if (found != 99) return 2;

    u128 answer = 0;
    for (int n = 2; n <= 100; ++n) answer += minimal[n];
    cout << to_string128(answer) << '\n';
    return 0;
}
"""


def solve():
    with tempfile.TemporaryDirectory(prefix="p563_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p563.cpp"
        exe = tmp_path / "p563"
        cpp.write_text(SOURCE)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(cpp), "-o", str(exe)],
            check=True,
        )
        result = subprocess.run(
            [str(exe)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return result.stdout.strip()


if __name__ == "__main__":
    print(solve())
