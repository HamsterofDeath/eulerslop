#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

static inline int64 isqrtll(int64 n) {
    int64 root = static_cast<int64>(sqrt(static_cast<long double>(n)));
    while ((__int128)(root + 1) * (root + 1) <= n) {
        ++root;
    }
    while ((__int128)root * root > n) {
        --root;
    }
    return root;
}

static inline int64 sum_squares(int64 n) {
    return n * (n + 1) * (2 * n + 1) / 6;
}

static inline int64 sum_squares_range(int64 lo, int64 hi) {
    if (hi < lo) {
        return 0;
    }
    return sum_squares(hi) - sum_squares(lo - 1);
}

static inline int64 sum_squares_with_parity(int64 lo, int64 hi, int parity) {
    if ((lo & 1) != parity) {
        ++lo;
    }
    if ((hi & 1) != parity) {
        --hi;
    }
    if (hi < lo) {
        return 0;
    }

    if (parity == 0) {
        return 4 * sum_squares_range(lo / 2, hi / 2);
    }

    int64 a = (lo + 1) / 2;
    int64 b = (hi + 1) / 2;
    int64 count = b - a + 1;
    return 4 * sum_squares_range(a, b) - 2 * (a + b) * count + count;
}

static vector<int> floor_sqrts(int limit) {
    vector<int> result(limit + 1);
    for (int i = 1, root = 0; i <= limit; ++i) {
        while (1LL * (root + 1) * (root + 1) <= i) {
            ++root;
        }
        result[i] = root;
    }
    return result;
}

static vector<int> squarefree_kernels(int limit) {
    vector<int> spf(limit + 1);
    for (int i = 2; i <= limit; ++i) {
        if (spf[i] != 0) {
            continue;
        }
        spf[i] = i;
        if (1LL * i * i <= limit) {
            for (int64 j = 1LL * i * i; j <= limit; j += i) {
                if (spf[j] == 0) {
                    spf[j] = i;
                }
            }
        }
    }

    vector<int> kernel(limit + 1);
    kernel[1] = 1;
    for (int i = 2; i <= limit; ++i) {
        int x = i;
        int k = 1;
        while (x > 1) {
            int p = spf[x];
            int odd = 0;
            while (x % p == 0) {
                x /= p;
                odd ^= 1;
            }
            if (odd) {
                k *= p;
            }
        }
        kernel[i] = k;
    }
    return kernel;
}

static inline int combine_squarefree(int a, int b) {
    int g = gcd(a, b);
    return (a / g) * (b / g);
}

static long long solve_for(int n) {
    int max_gap = static_cast<int>(sqrt(3.0L) * n) + 10;
    int max_quotient = 3 * max_gap + 10;

    vector<int> fsqrt = floor_sqrts(max_quotient);
    vector<int> csqrt(max_quotient + 1);
    for (int i = 1; i <= max_quotient; ++i) {
        int r = fsqrt[i];
        csqrt[i] = (r * r == i) ? r : r + 1;
    }

    vector<int> kernel = squarefree_kernels(max_gap);
    int64 area_limit_squared = 1LL * n * n;
    __int128 total = 0;

    /*
      For integer sides, Brahmagupta's maximal area is sqrt(x*y*z*w), where
      x >= y >= z >= w are positive integer semiperimeter gaps and x+y+z+w
      is even.  For each (w,z,y), x must have the squarefree kernel of y*z*w,
      so all valid x are k*t^2 in one interval and can be summed directly.
    */
    for (int w = 1; w <= max_gap; ++w) {
        for (int z = w; z <= max_gap; ++z) {
            if ((__int128)z * z * w * w > area_limit_squared) {
                break;
            }

            int y_max = static_cast<int>(isqrtll(area_limit_squared / (1LL * z * w)));
            int zw_kernel = combine_squarefree(kernel[z], kernel[w]);

            for (int y = z; y <= y_max; ++y) {
                int64 high_by_area = area_limit_squared / (1LL * y * z * w);
                int64 high_by_quad = 1LL * y + z + w - 1;
                int64 high = min(high_by_area, high_by_quad);
                if (high < y) {
                    continue;
                }

                int k = combine_squarefree(kernel[y], zw_kernel);
                int64 low_quotient = (y + k - 1) / k;
                int64 high_quotient = high / k;
                if (high_quotient < low_quotient) {
                    continue;
                }

                int64 lo = csqrt[low_quotient];
                int64 hi = fsqrt[high_quotient];
                if (hi < lo) {
                    continue;
                }

                int needed_parity = (y + z + w) & 1;
                int64 count = 0;
                int64 x_sum = 0;
                if ((k & 1) == 0) {
                    if (needed_parity != 0) {
                        continue;
                    }
                    count = hi - lo + 1;
                    x_sum = 1LL * k * sum_squares_range(lo, hi);
                } else {
                    int64 first = lo;
                    int64 last = hi;
                    if ((first & 1) != needed_parity) {
                        ++first;
                    }
                    if ((last & 1) != needed_parity) {
                        --last;
                    }
                    if (last < first) {
                        continue;
                    }
                    count = (last - first) / 2 + 1;
                    x_sum = 1LL * k * sum_squares_with_parity(lo, hi, needed_parity);
                }

                total += x_sum + (__int128)count * (y + z + w);
            }
        }
    }

    return static_cast<long long>(total);
}

int main(int argc, char** argv) {
    int n = 1000000;
    if (argc > 1) {
        n = stoi(argv[1]);
    }
    cout << solve_for(n) << '\n';
    return 0;
}
