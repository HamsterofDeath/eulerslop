#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

using namespace std;

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

void add_factorisation(int value, vector<pair<int, int>>& factors) {
    while (value > 1) {
        const int prime = smallest_prime_factor[value];
        int exponent = 0;
        while (value % prime == 0) {
            value /= prime;
            ++exponent;
        }
        factors.push_back({prime, exponent});
    }
}

void generate_divisors(
    const vector<pair<int, int>>& factors,
    int index,
    long long current,
    vector<long long>& divisors
) {
    if (index == static_cast<int>(factors.size())) {
        divisors.push_back(current);
        return;
    }
    const auto [prime, exponent] = factors[index];
    long long multiplier = 1;
    for (int i = 0; i <= exponent; ++i) {
        generate_divisors(factors, index + 1, current * multiplier, divisors);
        multiplier *= prime;
    }
}

long long pentagonal(long long n) {
    return n * (3 * n - 1) / 2;
}

long long first_pentagonal_with_more_than(int threshold, int search_limit) {
    build_sieve(3 * search_limit);

    vector<unsigned short> representations(search_limit + 1, 0);
    vector<pair<int, int>> factors;
    vector<pair<int, int>> merged;
    vector<long long> divisors;

    for (int b = 1; b <= search_limit; ++b) {
        factors.clear();
        add_factorisation(3 * b - 1, factors);
        add_factorisation(3 * b, factors);
        sort(factors.begin(), factors.end());

        merged.clear();
        for (const auto [prime, exponent] : factors) {
            if (!merged.empty() && merged.back().first == prime) {
                merged.back().second += exponent;
            } else {
                merged.push_back({prime, exponent});
            }
        }

        divisors.clear();
        generate_divisors(merged, 0, 1, divisors);

        const long long m = 1LL * (3 * b - 1) * (3 * b);
        const long long max_other = 6LL * b - 1;
        for (const long long y : divisors) {
            if (y * y > m) {
                continue;
            }
            const long long x = m / y;
            const long long other = x - y;
            if (other <= 0 || other > max_other) {
                continue;
            }
            const long long target = x + y;
            if (other % 6 == 5 && target % 6 == 5) {
                const int n = static_cast<int>((target + 1) / 6);
                if (n <= search_limit) {
                    ++representations[n];
                }
            }
        }

        // Once b has been processed, all representations for P_{b-1} have
        // been seen because both summand indices are strictly smaller.
        if (b > 1 && representations[b - 1] > threshold) {
            return pentagonal(b - 1);
        }
    }
    return -1;
}

}  // namespace

int main() {
    if (first_pentagonal_with_more_than(1, 1000) != 3577) {
        return 1;
    }
    if (first_pentagonal_with_more_than(2, 1000) != 107602) {
        return 1;
    }
    cout << first_pentagonal_with_more_than(100, 30'000'000) << '\n';
    return 0;
}
