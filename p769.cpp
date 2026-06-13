#include <algorithm>
#include <cmath>
#include <iostream>
#include <utility>
#include <vector>

using namespace std;

using i64 = long long;
using i128 = __int128_t;

namespace {

vector<int> smallest_prime_factor;

void build_sieve(int n) {
    smallest_prime_factor.assign(n + 1, 0);
    for (int i = 2; i <= n; ++i) {
        if (smallest_prime_factor[i] != 0) {
            continue;
        }
        smallest_prime_factor[i] = i;
        if (1LL * i * i <= n) {
            for (long long j = 1LL * i * i; j <= n; j += i) {
                if (smallest_prime_factor[j] == 0) {
                    smallest_prime_factor[j] = i;
                }
            }
        }
    }
}

void squarefree_divisors(int q, vector<pair<int, int>>& divisors) {
    vector<int> primes;
    while (q > 1) {
        const int p = smallest_prime_factor[q];
        primes.push_back(p);
        while (q % p == 0) {
            q /= p;
        }
    }

    divisors.clear();
    divisors.push_back({1, 1});
    for (const int p : primes) {
        const int size = static_cast<int>(divisors.size());
        for (int i = 0; i < size; ++i) {
            divisors.push_back({divisors[i].first * p, -divisors[i].second});
        }
    }
}

i64 inverse_mod(i64 a, i64 mod) {
    i64 b = mod;
    i64 u = 1;
    i64 v = 0;
    while (b != 0) {
        const i64 t = a / b;
        a -= t * b;
        swap(a, b);
        u -= t * v;
        swap(u, v);
    }
    u %= mod;
    if (u < 0) {
        u += mod;
    }
    return u;
}

i64 count_progression(i64 left, i64 right, i64 mod, i64 residue) {
    if (left > right) {
        return 0;
    }
    residue %= mod;
    if (residue < 0) {
        residue += mod;
    }
    const i64 first = left + ((residue - left) % mod + mod) % mod;
    if (first > right) {
        return 0;
    }
    return (right - first) / mod + 1;
}

i64 count_coprime(i64 left, i64 right, const vector<pair<int, int>>& divisors) {
    i64 total = 0;
    for (const auto [d, mu] : divisors) {
        total += mu * (right / d - (left - 1) / d);
    }
    return total;
}

i64 count_coprime_class_13(
    i64 left,
    i64 right,
    int q,
    const vector<pair<int, int>>& divisors
) {
    if (q % 13 == 0) {
        return 0;
    }

    const i64 residue = (13 - q % 13) % 13;
    i64 total = 0;
    for (const auto [d, mu] : divisors) {
        const i64 t = residue * inverse_mod(d % 13, 13) % 13;
        total += mu * count_progression(left, right, 13LL * d, d * t);
    }
    return total;
}

i64 x_form(i64 p, i64 q) {
    return p * p - 6 * p * q + 6 * q * q;
}

i64 z_form(i64 p, i64 q) {
    return -3 * p * p + 7 * p * q - 3 * q * q;
}

vector<pair<i64, i64>> valid_ranges(int q, i64 z_bound) {
    const i64 left = q + 1;

    const long double alpha = 3.0L - sqrtl(3.0L);
    i64 right = static_cast<i64>(floor(alpha * q)) + 3;
    while (right > q && x_form(right, q) <= 0) {
        --right;
    }
    while (x_form(right + 1, q) > 0) {
        ++right;
    }

    if (left > right || 1LL * q * q > z_bound) {
        return {};
    }

    const i128 discriminant = static_cast<i128>(13) * q * q
        - static_cast<i128>(12) * z_bound;
    if (discriminant <= 0) {
        return {{left, right}};
    }

    i64 root = static_cast<i64>(sqrt(static_cast<long double>(discriminant)));
    while (static_cast<i128>(root + 1) * (root + 1) <= discriminant) {
        ++root;
    }
    while (static_cast<i128>(root) * root > discriminant) {
        --root;
    }

    vector<pair<i64, i64>> ranges;

    i64 end_first = (7LL * q - root) / 6 + 3;
    while (end_first >= left && z_form(end_first, q) > z_bound) {
        --end_first;
    }
    while (end_first + 1 <= right && z_form(end_first + 1, q) <= z_bound) {
        ++end_first;
    }
    if (left <= min(right, end_first)) {
        ranges.push_back({left, min(right, end_first)});
    }

    i64 start_second = (7LL * q + root) / 6 - 3;
    while (start_second <= right && z_form(start_second, q) > z_bound) {
        ++start_second;
    }
    while (start_second - 1 >= left && z_form(start_second - 1, q) <= z_bound) {
        --start_second;
    }
    if (max(left, start_second) <= right) {
        ranges.push_back({max(left, start_second), right});
    }

    return ranges;
}

i64 count_representations(i64 n) {
    const int q_limit = static_cast<int>(sqrt(static_cast<long double>(13) * n)) + 5;
    build_sieve(q_limit);

    vector<pair<int, int>> divisors;
    i64 total = 0;
    for (int q = 1; q <= q_limit; ++q) {
        squarefree_divisors(q, divisors);

        if (1LL * q * q <= n) {
            for (const auto [left, right] : valid_ranges(q, n)) {
                total += count_coprime(left, right, divisors)
                    - count_coprime_class_13(left, right, q, divisors);
            }
        }

        for (const auto [left, right] : valid_ranges(q, 13 * n)) {
            total += count_coprime_class_13(left, right, q, divisors);
        }
    }
    return total;
}

}  // namespace

int main() {
    if (count_representations(1'000) != 142) {
        return 1;
    }
    if (count_representations(1'000'000) != 142'463) {
        return 1;
    }
    cout << count_representations(100'000'000'000'000LL) << '\n';
    return 0;
}
