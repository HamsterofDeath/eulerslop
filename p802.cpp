// Project Euler 802: f(z)=z^2-z+i*pi.  The root sum of f^k(z)-z is 2 for
// k=1 and 2^(k-1) afterwards; exact periods are recovered by Mobius inversion.
#include <cstdint>
#include <cstdio>
#include <vector>

using namespace std;

static const int MOD = 1020340567;

static vector<int> mobius_prefix(int n) {
    vector<int> primes, lp(n + 1), mu(n + 1), prefix(n + 1);
    mu[1] = 1;
    for (int i = 2; i <= n; ++i) {
        if (lp[i] == 0) {
            lp[i] = i;
            primes.push_back(i);
            mu[i] = -1;
        }
        for (int p : primes) {
            long long x = 1LL * p * i;
            if (x > n || p > lp[i]) break;
            lp[(int)x] = p;
            if (p == lp[i]) {
                mu[(int)x] = 0;
                break;
            }
            mu[(int)x] = -mu[i];
        }
    }
    prefix[1] = 1;
    for (int i = 2; i <= n; ++i) prefix[i] = prefix[i - 1] + mu[i];
    return prefix;
}

static int p_value(int n) {
    vector<int> mertens = mobius_prefix(n);
    int64_t answer = 0;
    int64_t power = 1;  // 2^(m-1)
    for (int m = 1; m <= n; ++m) {
        int64_t divisor_sum = mertens[n / m] % MOD;
        if (divisor_sum < 0) divisor_sum += MOD;
        int64_t root_sum = (m == 1) ? 2 : power;
        answer = (answer + root_sum * divisor_sum) % MOD;
        power = (power * 2) % MOD;
    }
    return (int)answer;
}

int main() {
    if (p_value(1) != 2 || p_value(2) != 2 || p_value(3) != 4) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%d\n", p_value(10000000));
    return 0;
}
