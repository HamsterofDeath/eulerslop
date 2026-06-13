#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using i64 = long long;

constexpr int kDefaultN = 24'680;
constexpr i64 kMod = 1'020'202'009LL;

int parse_n(int argc, char** argv) {
    int n = kDefaultN;
    for (int i = 1; i < argc; ++i) {
        const std::string arg(argv[i]);
        const std::string prefix = "--n=";
        if (arg.rfind(prefix, 0) != 0) {
            throw std::invalid_argument("unknown argument: " + arg);
        }

        n = 0;
        for (char c : arg.substr(prefix.size())) {
            if (c < '0' || c > '9') {
                throw std::invalid_argument("invalid --n value");
            }
            n = 10 * n + (c - '0');
        }
    }
    return n;
}

i64 solve(int n) {
    std::vector<i64> prev(n + 1);
    std::vector<i64> curr(n + 1);
    prev[0] = 1;

    for (int row = 1; row <= n; ++row) {
        curr[0] = 0;
        i64 running = 0;
        for (int k = 1; k <= row; ++k) {
            running += prev[row - k];
            if (running >= kMod) {
                running -= kMod;
            }
            curr[k] = running;
        }
        prev.swap(curr);
    }

    return prev[n];
}

}  // namespace

int main(int argc, char** argv) {
    try {
        std::cout << solve(parse_n(argc, argv)) << '\n';
    } catch (const std::exception& exc) {
        std::cerr << exc.what() << '\n';
        return 1;
    }
    return 0;
}
