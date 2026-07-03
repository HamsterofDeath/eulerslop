// Project Euler 841: along a ray, the q crossed star edges alternate shaded
// and unshaded.  Integrating sec^2 over the p-fold symmetric sector gives the
// alternating tangent sum below.
#include <cmath>
#include <cstdio>
#include <iomanip>
#include <iostream>
#include <vector>

using namespace std;

static long double area(long long p, long long q) {
    const long double pi = acosl(-1.0L);
    long double sum = 0.0L;
    long double prev = 0.0L;
    int sign = ((q - 1) & 1LL) ? -1 : 1;
    long double c = 0.0L;  // Kahan compensation.
    for (long long t = 0; t < q; ++t) {
        long double cur = tanl((long double)(t + 1) * pi / (long double)p);
        long double term = (long double)sign * (cur - prev) - c;
        long double next = sum + term;
        c = (next - sum) - term;
        sum = next;
        sign = -sign;
        prev = cur;
    }
    return (long double)p * sum;
}

int main() {
    long double exact = 24.0L * (sqrtl(2.0L) - 1.0L);
    if (fabsl(area(8, 3) - exact) > 1e-12L ||
        fabsl(area(130021, 50008) - 10.9210371479L) > 1e-9L) {
        fprintf(stderr, "self-test failed: %.12Lf %.12Lf\n", area(8, 3),
                area(130021, 50008));
        return 1;
    }

    vector<long long> fib(36);
    fib[1] = fib[2] = 1;
    for (int i = 3; i < (int)fib.size(); ++i) fib[i] = fib[i - 1] + fib[i - 2];

    long double total = 0.0L;
    for (int n = 3; n <= 34; ++n) total += area(fib[n + 1], fib[n - 1]);
    cout << fixed << setprecision(10) << (double)total << "\n";
    return 0;
}
