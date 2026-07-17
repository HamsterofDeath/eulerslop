// Project Euler 841: along a ray, the q crossed star edges alternate shaded
// and unshaded.  Integrating sec^2 over the p-fold symmetric sector gives an
// alternating sum of tangent increments.  Pair adjacent increments
// analytically so that millions of nearly equal terms are never subtracted.
#include <cmath>
#include <cstdio>
#include <iomanip>
#include <iostream>
#include <vector>

using namespace std;

static long double area(long long p, long long q) {
    const long double pi = acosl(-1.0L);
    const long double x = pi / (long double)p;
    const long double twice_sin_squared = 2.0L * sinl(x) * sinl(x);
    long double sum = 0.0L;
    long double c = 0.0L;  // Kahan compensation.

    // For even q, pair Delta_2-Delta_1, Delta_4-Delta_3, ...
    // For odd q, retain Delta_1 and pair Delta_3-Delta_2, ...
    long long first_center;
    if (q & 1LL) {
        sum = tanl(x);
        first_center = 2;
    } else {
        first_center = 1;
    }

    for (long long center_index = first_center; center_index < q;
         center_index += 2) {
        long double center = (long double)center_index * x;
        long double paired =
            twice_sin_squared * tanl(center) /
            (cosl(center - x) * cosl(center + x));
        long double term = paired - c;
        long double next = sum + term;
        c = (next - sum) - term;
        sum = next;
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
    cout << fixed << setprecision(10) << total << "\n";
    return 0;
}
