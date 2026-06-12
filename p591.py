#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from decimal import Decimal, ROUND_HALF_UP, getcontext
from pathlib import Path


LIMIT = 10**13
PI = Decimal(
    "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
)


CPP_SOURCE = r"""
#include <bits/stdc++.h>
#include <quadmath.h>
using namespace std;

static const long long LIMIT = 10000000000000LL;
static const int KEEP = 5000;

struct Baby {
    long double value;
    int index;
};

struct Candidate {
    long double distance;
    long long b;
    int sign;
};

struct WorseCandidate {
    bool operator()(const Candidate& a, const Candidate& b) const {
        return a.distance < b.distance;
    }
};

static __float128 fracq(__float128 x) {
    x -= floorq(x);
    if (x < 0) x += 1;
    return x;
}

static long double fracld(long double x) {
    x -= floorl(x);
    if (x < 0) x += 1;
    return x;
}

int main() {
    cout.setf(ios::fixed);
    cout << setprecision(0);

    __float128 pi = acosq(-1);
    __float128 pi_frac = fracq(pi);

    for (int d = 2; d < 100; ++d) {
        int root = (int)sqrt(d);
        if (root * root == d) continue;

        __float128 alpha = sqrtq((__float128)d);
        __float128 frac_alpha = fracq(alpha);
        long long max_b = min(
            LIMIT,
            (long long)floorq(((__float128)LIMIT + 4) / alpha)
        );

        int block = (int)(sqrtq((__float128)max_b) + 1);
        vector<Baby> babies;
        babies.reserve(block);

        __float128 x = 0;
        for (int i = 0; i < block; ++i) {
            babies.push_back({(long double)x, i});
            x = fracq(x + frac_alpha);
        }

        sort(babies.begin(), babies.end(), [](const Baby& a, const Baby& b) {
            return a.value < b.value;
        });

        auto circular_distance = [](long double a, long double b) {
            long double z = fabsl(a - b);
            return min(z, 1.0L - z);
        };

        priority_queue<Candidate, vector<Candidate>, WorseCandidate> best;
        auto push_candidate = [&](long double distance, long long b, int sign) {
            Candidate candidate{distance, b, sign};
            if ((int)best.size() < KEEP) {
                best.push(candidate);
            } else if (distance < best.top().distance) {
                best.pop();
                best.push(candidate);
            }
        };

        auto consider = [&](__float128 needq, long long giant, int sign) {
            long double need = fracld((long double)fracq(needq));
            int size = (int)babies.size();
            int pos = (int)(lower_bound(
                babies.begin(),
                babies.end(),
                need,
                [](const Baby& baby, long double value) {
                    return baby.value < value;
                }
            ) - babies.begin());

            for (int offset = -16; offset <= 16; ++offset) {
                int p = (pos + offset) % size;
                if (p < 0) p += size;
                long long b = giant * (long long)block + babies[p].index;
                if (b <= 0 || b > max_b) continue;
                push_candidate(circular_distance(babies[p].value, need), b, sign);
            }
        };

        __float128 step = fracq(frac_alpha * (__float128)block);
        __float128 base = 0;
        long long max_giant = (max_b + block - 1) / block;

        for (long long giant = 0; giant <= max_giant; ++giant) {
            consider(pi_frac - base, giant, +1);
            consider(-pi_frac - base, giant, -1);
            base = fracq(base + step);
        }

        vector<Candidate> candidates;
        while (!best.empty()) {
            candidates.push_back(best.top());
            best.pop();
        }
        sort(candidates.begin(), candidates.end(), [](const Candidate& a, const Candidate& b) {
            return a.distance < b.distance;
        });

        vector<pair<long long, int>> output;
        for (const auto& candidate : candidates) {
            pair<long long, int> key{candidate.b, candidate.sign};
            if (find(output.begin(), output.end(), key) == output.end()) {
                output.push_back(key);
            }
            if (output.size() >= 1000) break;
        }

        cout << "D " << d << " " << output.size() << '\n';
        for (auto [b, sign] : output) {
            cout << b << " " << sign << '\n';
        }
    }
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p591_{digest}.cpp"
    exe = root / f"p591_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            [
                "g++",
                "-O3",
                "-march=native",
                "-std=c++17",
                str(src),
                "-lquadmath",
                "-o",
                str(exe),
            ],
            check=True,
        )
    return exe


def nearest_integral_part(d, signed_b):
    square_root = Decimal(d).sqrt()
    value = PI - Decimal(signed_b) * square_root
    nearest = int(value.to_integral_value(rounding=ROUND_HALF_UP))

    best_error = None
    best_a = None
    for a in range(nearest - 2, nearest + 3):
        if abs(a) > LIMIT:
            continue
        error = abs(Decimal(a) + Decimal(signed_b) * square_root - PI)
        if best_error is None or error < best_error:
            best_error = error
            best_a = a
    return best_a, best_error


def solve():
    getcontext().prec = 90
    result = subprocess.run(
        [str(_binary())],
        check=True,
        capture_output=True,
        text=True,
    )

    lines = result.stdout.splitlines()
    index = 0
    total = 0
    integral_parts = {}

    while index < len(lines):
        header = lines[index].split()
        index += 1
        if not header:
            continue
        assert header[0] == "D"
        d = int(header[1])
        count = int(header[2])

        best_error = abs(Decimal(3) - PI)
        best_a = 3
        for _ in range(count):
            b0, sign = map(int, lines[index].split())
            index += 1
            a, error = nearest_integral_part(d, b0 * sign)
            if error < best_error:
                best_error = error
                best_a = a

        integral_parts[d] = best_a
        total += abs(best_a)

    assert brute_integral_part(2, 10) == 6
    assert brute_integral_part(5, 100) == -55
    assert integral_parts[2] == -6188084046055
    return total


def brute_integral_part(d, limit):
    getcontext().prec = 60
    square_root = Decimal(d).sqrt()
    best_error = None
    best_a = None
    for b in range(-limit, limit + 1):
        value = PI - Decimal(b) * square_root
        nearest = int(value.to_integral_value(rounding=ROUND_HALF_UP))
        for a in range(nearest - 1, nearest + 2):
            if abs(a) > limit:
                continue
            error = abs(Decimal(a) + Decimal(b) * square_root - PI)
            if best_error is None or error < best_error:
                best_error = error
                best_a = a
    return best_a


if __name__ == "__main__":
    print(solve())
