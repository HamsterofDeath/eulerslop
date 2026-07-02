// Project Euler 737: coin loop, number of coins for 2020 loops.
//
// All coin centres lie (in plan view) on the unit circle around the line.
// Placing greedily from the top of the final stack downwards, every
// suffix-balance constraint is tight: the centre of mass of the m coins
// above coin j sits exactly on coin j's boundary,
//   |S - m c_j| = m  =>  S . c_j = |S|^2 / (2m),
// where S is the (plan) vector sum of the m centres above.  So
//   c_j = (S/|S|) rotated backwards by beta, cos beta = |S|/(2m),
// and the intermediate stages of the bottom-up construction are then
// automatically balanced (partial suffixes lie further inward), as in the
// classic harmonic overhang stack.  The table contact is automatic:
// |CoM(all) - c_bottom| = (n-1)/n < 1.  Validated: 31 coins for 1 loop,
// 154 for 2 loops, 6947 for 10 loops.
#include <cmath>
#include <cstdio>

typedef long long i64;

static i64 find_n(double loops, i64 nmax) {
    const double goal = 2.0 * M_PI * loops;
    double Sx = 1.0, Sy = 0.0;      // sum of centres above current coin
    double cx = 1.0, cy = 0.0;      // previous (higher) coin centre
    double wind = 0.0;              // total winding (top minus current)
    for (i64 m = 1; m < nmax; ++m) {
        double r2 = Sx * Sx + Sy * Sy;
        double r = sqrt(r2);
        double cb = r / (2.0 * (double)m);
        if (cb > 1.0) cb = 1.0;
        double sb = sqrt(1.0 - cb * cb);
        // c = (S/r) * (cos beta, -sin beta)  (rotate backwards)
        double ux = Sx / r, uy = Sy / r;
        double nx = ux * cb + uy * sb;
        double ny = uy * cb - ux * sb;
        // winding increment = angle from new c to previous c (forward)
        double cross = nx * cy - ny * cx;   // sin of increment
        double dot = nx * cx + ny * cy;
        double d = atan2(cross, dot);
        wind += d;
        if (wind > goal) return m + 1;
        cx = nx; cy = ny;
        Sx += nx; Sy += ny;
    }
    return -1;
}

int main() {
    if (find_n(1.0, 100) != 31 || find_n(2.0, 300) != 154 ||
        find_n(10.0, 10000) != 6947) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%lld\n", find_n(2020.0, 2000000000LL));
    return 0;
}
