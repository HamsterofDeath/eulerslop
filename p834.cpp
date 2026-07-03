// Project Euler 834: the m-th term is divisible by n+m iff d=n+m divides
// n(n-1) and d, n(n-1)/d have opposite parity.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static vector<int> smallest_prime_factor(int limit) {
    vector<int> spf(limit + 1);
    for (int i = 0; i <= limit; ++i) spf[i] = i;
    for (int i = 2; (int64_t)i * i <= limit; ++i) {
        if (spf[i] != i) continue;
        for (int64_t j = (int64_t)i * i; j <= limit; j += i)
            if (spf[(int)j] == j) spf[(int)j] = i;
    }
    return spf;
}

static vector<pair<int, int>> factor_with_spf(int n, const vector<int>& spf) {
    vector<pair<int, int>> result;
    while (n > 1) {
        int p = spf[n], e = 0;
        while (n % p == 0) {
            n /= p;
            ++e;
        }
        result.push_back({p, e});
    }
    return result;
}

static vector<pair<int, int>> merged_factorization(
    int a, int b, const vector<int>& spf) {
    vector<pair<int, int>> f = factor_with_spf(a, spf);
    vector<pair<int, int>> g = factor_with_spf(b, spf);
    for (auto [p, e] : g) {
        bool found = false;
        for (auto& item : f) {
            if (item.first == p) {
                item.second += e;
                found = true;
                break;
            }
        }
        if (!found) f.push_back({p, e});
    }
    sort(f.begin(), f.end());
    return f;
}

static void divisors_rec(const vector<pair<int, int>>& f, int idx, uint64_t current,
                         vector<uint64_t>& out) {
    if (idx == (int)f.size()) {
        out.push_back(current);
        return;
    }
    auto [p, e] = f[idx];
    uint64_t value = current;
    for (int i = 0; i <= e; ++i) {
        divisors_rec(f, idx + 1, value, out);
        value *= (uint64_t)p;
    }
}

static uint64_t t_value(int n, const vector<int>& spf) {
    uint64_t product = (uint64_t)n * (n - 1);
    vector<pair<int, int>> f = merged_factorization(n, n - 1, spf);
    vector<uint64_t> divisors;
    divisors_rec(f, 0, 1, divisors);

    uint64_t total = 0;
    for (uint64_t d : divisors) {
        if (d <= (uint64_t)n) continue;
        uint64_t q = product / d;
        if (((d + q) & 1ULL) == 1) total += d - n;
    }
    return total;
}

static unsigned __int128 u_value(int limit) {
    vector<int> spf = smallest_prime_factor(limit);
    unsigned __int128 total = 0;
    for (int n = 3; n <= limit; ++n) total += t_value(n, spf);
    return total;
}

static string to_string_u128(unsigned __int128 value) {
    if (value == 0) return "0";
    string out;
    while (value) {
        out.push_back(char('0' + value % 10));
        value /= 10;
    }
    reverse(out.begin(), out.end());
    return out;
}

int main() {
    vector<int> spf = smallest_prime_factor(100);
    if (t_value(10, spf) != 148 || t_value(100, spf) != 21828 ||
        u_value(100) != 612572) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    cout << to_string_u128(u_value(1234567)) << "\n";
    return 0;
}
