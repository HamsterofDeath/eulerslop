#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numbers>
#include <vector>

static constexpr long double PI =
    3.141592653589793238462643383279502884L;

static long double angle_sum(const std::vector<int>& counts, long double radius) {
    long double total = 0.0L;
    for (int excess = 0; excess < (int)counts.size(); ++excess) {
        if (counts[excess] == 0) continue;
        const long double side = (long double)excess + 1.0L;
        long double ratio = side / (2.0L * radius);
        if (ratio > 1.0L) ratio = 1.0L;
        total += (long double)counts[excess] * std::asin(ratio);
    }
    return total;
}

static long double maximal_area(const std::vector<int>& counts) {
    int max_side = 1;
    for (int excess = 0; excess < (int)counts.size(); ++excess) {
        if (counts[excess]) max_side = excess + 1;
    }

    long double low = (long double)max_side / 2.0L;
    long double high = (long double)max_side;
    const bool center_inside = angle_sum(counts, low) >= PI;

    if (center_inside) {
        while (angle_sum(counts, high) > PI) high *= 2.0L;

        for (int iter = 0; iter < 120; ++iter) {
            const long double mid = (low + high) / 2.0L;
            if (angle_sum(counts, mid) > PI) {
                low = mid;
            } else {
                high = mid;
            }
        }
    } else {
        auto outside_difference = [&](long double radius) {
            long double other = 0.0L;
            bool skipped_longest = false;
            for (int excess = 0; excess < (int)counts.size(); ++excess) {
                int count = counts[excess];
                if (count == 0) continue;
                const long double side = (long double)excess + 1.0L;
                if (!skipped_longest && excess + 1 == max_side) {
                    --count;
                    skipped_longest = true;
                }
                if (count > 0) other += (long double)count * std::asin(side / (2.0L * radius));
            }
            return other - std::asin((long double)max_side / (2.0L * radius));
        };

        while (outside_difference(high) < 0.0L) high *= 2.0L;

        for (int iter = 0; iter < 120; ++iter) {
            const long double mid = (low + high) / 2.0L;
            if (outside_difference(mid) < 0.0L) {
                low = mid;
            } else {
                high = mid;
            }
        }
    }

    const long double radius = high;
    long double area = 0.0L;
    bool skipped_longest = false;
    for (int excess = 0; excess < (int)counts.size(); ++excess) {
        if (counts[excess] == 0) continue;
        const long double side = (long double)excess + 1.0L;
        int sign_count = counts[excess];
        if (!center_inside && !skipped_longest && excess + 1 == max_side) {
            area -= side * std::sqrt(4.0L * radius * radius - side * side) / 4.0L;
            --sign_count;
            skipped_longest = true;
        }
        area += (long double)sign_count * side *
                std::sqrt(4.0L * radius * radius - side * side) / 4.0L;
    }
    return area;
}

static long double multinomial_weight(int sides, const std::vector<int>& counts) {
    long double log_weight = std::lgammal((long double)sides + 1.0L);
    for (int count : counts) {
        log_weight -= std::lgammal((long double)count + 1.0L);
    }
    return std::exp(log_weight);
}

static long double composition_count(int n) {
    // Number of ordered positive n-part compositions of 2n-3.
    return std::exp(std::lgammal((long double)(2 * n - 3))
                    - std::lgammal((long double)n)
                    - std::lgammal((long double)(n - 2)));
}

static void accumulate_expected_area(int excess,
                                     int remaining_excess,
                                     int remaining_sides,
                                     int n,
                                     std::vector<int>& counts,
                                     long double& weighted_sum) {
    if (excess == 0) {
        if (remaining_excess != 0) return;
        counts[0] = remaining_sides;
        const long double weight = multinomial_weight(n, counts);
        weighted_sum += weight * maximal_area(counts);
        counts[0] = 0;
        return;
    }

    const int max_count = std::min(remaining_sides, remaining_excess / excess);
    for (int count = 0; count <= max_count; ++count) {
        counts[excess] = count;
        accumulate_expected_area(excess - 1,
                                 remaining_excess - count * excess,
                                 remaining_sides - count,
                                 n,
                                 counts,
                                 weighted_sum);
    }
    counts[excess] = 0;
}

static long double E(int n) {
    std::vector<int> counts((size_t)n - 2, 0);
    long double weighted_sum = 0.0L;
    accumulate_expected_area(n - 3, n - 3, n, n, counts, weighted_sum);
    return weighted_sum / composition_count(n);
}

static long double S(int limit) {
    long double total = 0.0L;
    for (int n = 3; n <= limit; ++n) total += E(n);
    return total;
}

int main(int argc, char** argv) {
    int limit = argc > 1 ? std::stoi(argv[1]) : 50;
    std::cout << std::fixed << std::setprecision(6) << S(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p564_{digest}.cpp"
    exe = root / f"p564_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++20", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def S(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def solve():
    assert S(3) == "0.433013"
    assert S(4) == "1.732051"
    assert S(5) == "4.604767"
    assert S(10) == "66.955511"
    return S(50)


if __name__ == "__main__":
    print(solve())
