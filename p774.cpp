// Project Euler 774: conjunctive sequences, c(123, 123456789) mod 998244353.
//
// f_t(x) = number of conjunctive sequences of length t ending at x (x <= b).
// f_{t+1}(y) = T_t - sum_{x <= b, x AND y = 0} f_t(x)
//            = T_t - SOS(f_t)(~y),
// where SOS is the subset-sum (zeta) transform over the 27-bit cube.
// Direct simulation: 122 iterations of a 27-pass SOS over 2^27 cells,
// parallelized per pass.  Verified against c(3,4)=18, c(10,6)=2496120,
// c(100,200) = 268159379 (mod 998244353).
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <thread>
#include <vector>

using namespace std;
typedef uint32_t u32;
typedef unsigned long long u64;

static const u32 MOD = 998244353;

static int NTH;

// in-place subset-sum transform over 2^bits on u32 mod-p values, fused in
// groups of <=7 bits per memory sweep.  Group work happens branchlessly in
// u64 (values < 2^37; one reduction at store).  For large strides the group
// is processed via contiguous scratch tiles to avoid power-of-two cache
// aliasing, which otherwise dominates the runtime.
static const size_t TILE = 2048;

static void sos_group_tiled(u32* a, size_t inner, size_t lanes, size_t nblocks,
                            size_t blocksz) {
    size_t tiles_per_block = inner / TILE;
    size_t total_tiles = nblocks * tiles_per_block;
    vector<thread> ths;
    for (int t = 0; t < NTH; ++t)
        ths.emplace_back([=]() {
            vector<u64> scratch(lanes * TILE);
            for (size_t ti = t; ti < total_tiles; ti += (size_t)NTH) {
                size_t blk = ti / tiles_per_block, tf = ti % tiles_per_block;
                u32* bp = a + blk * blocksz + tf * TILE;
                for (size_t l = 0; l < lanes; ++l) {
                    u32* src = bp + l * inner;
                    u64* dst = scratch.data() + l * TILE;
                    for (size_t i = 0; i < TILE; ++i) dst[i] = src[i];
                }
                for (size_t st = 1; st < lanes; st <<= 1)
                    for (size_t b2 = 0; b2 < lanes; b2 += 2 * st)
                        for (size_t j = 0; j < st; ++j) {
                            u64* hi = scratch.data() + (b2 + st + j) * TILE;
                            u64* lo = scratch.data() + (b2 + j) * TILE;
                            for (size_t i = 0; i < TILE; ++i) hi[i] += lo[i];
                        }
                for (size_t l = 0; l < lanes; ++l) {
                    u64* src = scratch.data() + l * TILE;
                    u32* dst = bp + l * inner;
                    for (size_t i = 0; i < TILE; ++i)
                        dst[i] = (u32)(src[i] % MOD);
                }
            }
        });
    for (auto& th : ths) th.join();
}

static void sos(u32* a, int bits) {
    size_t n = (size_t)1 << bits;
    for (int base = 0; base < bits; base += 7) {
        int g = min(7, bits - base);
        size_t inner = (size_t)1 << base;
        size_t lanes = (size_t)1 << g;
        size_t blocksz = inner << g;
        size_t nblocks = n / blocksz;
        if (inner >= TILE) {
            sos_group_tiled(a, inner, lanes, nblocks, blocksz);
            continue;
        }
        vector<thread> ths;
        for (int t = 0; t < NTH; ++t)
            ths.emplace_back([=]() {
                u64 buf[128];
                for (size_t blk = t; blk < nblocks; blk += (size_t)NTH) {
                    u32* base_p = a + blk * blocksz;
                    for (size_t off = 0; off < inner; ++off) {
                        u32* p = base_p + off;
                        for (size_t l = 0; l < lanes; ++l) buf[l] = p[l * inner];
                        for (size_t st = 1; st < lanes; st <<= 1)
                            for (size_t b2 = 0; b2 < lanes; b2 += 2 * st)
                                for (size_t i = 0; i < st; ++i)
                                    buf[b2 + st + i] += buf[b2 + i];
                        for (size_t l = 0; l < lanes; ++l)
                            p[l * inner] = (u32)(buf[l] % MOD);
                    }
                }
            });
        for (auto& th : ths) th.join();
    }
}

static u32 solve(u32 b, int nsteps) {
    int bits = 0;
    while ((1u << bits) <= b) ++bits;
    size_t n = (size_t)1 << bits;
    u32 full = (u32)(n - 1);
    vector<u32> f(n), w(n);
    for (size_t x = 0; x <= b; ++x) f[x] = 1;
    for (size_t x = b + 1; x < n; ++x) f[x] = 0;
    for (int step = 1; step < nsteps; ++step) {
        // T = sum f
        u64 T = 0;
        for (size_t x = 0; x <= b; ++x) {
            T += f[x];
            if (T >= (u64)MOD << 32) T -= (u64)MOD << 32;
        }
        u32 Tm = (u32)(T % MOD);
        {
            vector<thread> ths;
            for (int t = 0; t < NTH; ++t)
                ths.emplace_back([&, t]() {
                    size_t lo = t * n / NTH, hi = (t + 1) * n / NTH;
                    for (size_t i = lo; i < hi; ++i) w[i] = f[i];
                });
            for (auto& th : ths) th.join();
        }
        sos(w.data(), bits);
        // f'(y) = T - w[~y] for y <= b ; 0 otherwise
        vector<thread> ths;
        for (int t = 0; t < NTH; ++t)
            ths.emplace_back([&, t]() {
                size_t lo = (size_t)t * (b + 1) / NTH;
                size_t hi = (size_t)(t + 1) * (b + 1) / NTH;
                for (size_t y = lo; y < hi; ++y) {
                    u32 v = Tm + MOD - w[(~(u32)y) & full];
                    if (v >= MOD) v -= MOD;
                    f[y] = v;
                }
            });
        for (auto& th : ths) th.join();
        fill(f.begin() + b + 1, f.end(), 0);
    }
    u64 T = 0;
    for (size_t x = 0; x <= b; ++x) T = (T + f[x]) % MOD;
    return (u32)T;
}

int main() {
    NTH = max(1u, thread::hardware_concurrency());
    if (solve(4, 3) != 18 || solve(6, 10) != 2496120 ||
        solve(200, 100) != 268159379) {
        fprintf(stderr, "self-test failed: %u %u %u\n", solve(4, 3),
                solve(6, 10), solve(200, 100));
        return 1;
    }
    printf("%u\n", solve(123456789, 123));
    return 0;
}
