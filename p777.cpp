#include <algorithm>
#include <cmath>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

using namespace std;

using i64 = long long;
using i128 = __int128_t;

namespace {

vector<int> mobius_values(int n) {
    vector<int> mu(n + 1);
    vector<int> primes;
    vector<int> composite(n + 1);
    mu[1] = 1;

    for (int i = 2; i <= n; ++i) {
        if (!composite[i]) {
            primes.push_back(i);
            mu[i] = -1;
        }
        for (const int p : primes) {
            const long long v = 1LL * i * p;
            if (v > n) {
                break;
            }
            composite[v] = 1;
            if (i % p == 0) {
                mu[v] = 0;
                break;
            }
            mu[v] = -mu[i];
        }
    }
    return mu;
}

i64 triangle(i64 n) {
    return n * (n + 1) / 2;
}

i128 numerator_times_four(int m) {
    const vector<int> mu = mobius_values(m);
    const vector<int> moduli = {1, 2, 5, 10};

    vector<vector<i64>> coprime_count(4, vector<i64>(m + 1));
    vector<vector<i64>> coprime_sum(4, vector<i64>(m + 1));

    for (int idx = 0; idx < 4; ++idx) {
        const int r = moduli[idx];
        for (int d = 1; d <= m; ++d) {
            if (mu[d] == 0) {
                continue;
            }

            const i64 limit = m / (1LL * r * d);
            const i64 count_term = limit;
            const i64 sum_term = 1LL * r * d * triangle(limit);
            if (count_term == 0 && sum_term == 0) {
                continue;
            }

            for (int a = d; a <= m; a += d) {
                coprime_count[idx][a] += mu[d] * count_term;
                coprime_sum[idx][a] += mu[d] * sum_term;
            }
        }
    }

    // The r = 1 tables include b = 1; the problem sums over b >= 2.
    for (int a = 2; a <= m; ++a) {
        --coprime_count[0][a];
        --coprime_sum[0][a];
    }

    i128 total = 0;
    for (int a = 2; a <= m; ++a) {
        const i64 all_count = coprime_count[0][a];
        const i64 all_sum = coprime_sum[0][a];

        // Base case: the two crossing families are disjoint.
        total += static_cast<i128>(8LL * a - 6) * all_sum
            - static_cast<i128>(6LL * a) * all_count;

        // If 10 divides a*b, the two crossing families coincide.  Add the
        // difference between the coincident-family formula and the base one.
        const int missing_factor = 10 / gcd(10, a);
        const int idx = missing_factor == 1 ? 0 : missing_factor == 2 ? 1
            : missing_factor == 5                          ? 2
                                                            : 3;
        const i64 special_count = coprime_count[idx][a];
        const i64 special_sum = coprime_sum[idx][a];
        total += static_cast<i128>(-6LL * a + 3) * special_sum
            + static_cast<i128>(3LL * a + 4) * special_count;
    }
    return total;
}

i128 power10(int exponent) {
    i128 result = 1;
    while (exponent-- > 0) {
        result *= 10;
    }
    return result;
}

string to_scientific_10_digits(i128 numerator4) {
    string digits;
    for (i128 x = numerator4; x > 0; x /= 10) {
        digits.push_back(static_cast<char>('0' + x % 10));
    }
    reverse(digits.begin(), digits.end());

    int exponent = static_cast<int>(digits.size()) - 2;
    if (numerator4 >= 4 * power10(static_cast<int>(digits.size()) - 1)) {
        ++exponent;
    }

    const int shift = exponent - 9;
    i128 denominator = 4 * power10(shift);
    i128 rounded = numerator4 / denominator;
    const i128 remainder = numerator4 % denominator;
    if (2 * remainder >= denominator) {
        ++rounded;
    }

    if (rounded == 10'000'000'000LL) {
        rounded /= 10;
        ++exponent;
    }

    string mantissa = to_string(static_cast<long long>(rounded));
    while (mantissa.size() < 10) {
        mantissa.insert(mantissa.begin(), '0');
    }
    return mantissa.substr(0, 1) + "." + mantissa.substr(1) + "e"
        + to_string(exponent);
}

}  // namespace

int main() {
    if (numerator_times_four(10) != 6410) {
        return 1;
    }
    if (numerator_times_four(100) != 97'026'020) {
        return 1;
    }

    cout << to_scientific_10_digits(numerator_times_four(1'000'000)) << '\n';
    return 0;
}
