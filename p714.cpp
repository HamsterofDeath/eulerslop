#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

using u128 = unsigned __int128;

namespace {

constexpr int LIMIT = 50000;

std::vector<int> masks;
int mask_index[1024];
std::vector<std::array<int, 10>> next_index;
std::vector<std::array<unsigned char, 10>> allowed_digits;
std::vector<unsigned char> allowed_count;
int mask_count = 0;

std::vector<int> seen;
std::vector<int> parent;
std::vector<int> queue_ids;
std::vector<unsigned char> last_digit;
int stamp = 0;

std::string to_string_u128(u128 value) {
    if (value == 0) {
        return "0";
    }

    std::string result;
    while (value > 0) {
        result.push_back(static_cast<char>('0' + value % 10));
        value /= 10;
    }
    std::reverse(result.begin(), result.end());
    return result;
}

void prepare_masks() {
    std::memset(mask_index, -1, sizeof(mask_index));
    for (int mask = 1; mask < 1024; ++mask) {
        if (__builtin_popcount(static_cast<unsigned>(mask)) <= 2) {
            mask_index[mask] = static_cast<int>(masks.size());
            masks.push_back(mask);
        }
    }

    mask_count = static_cast<int>(masks.size());
    next_index.assign(mask_count, {});
    allowed_digits.assign(mask_count, {});
    allowed_count.assign(mask_count, 0);

    for (int i = 0; i < mask_count; ++i) {
        int mask = masks[i];
        int used = __builtin_popcount(static_cast<unsigned>(mask));
        for (int digit = 0; digit <= 9; ++digit) {
            if ((mask & (1 << digit)) || used < 2) {
                allowed_digits[i][allowed_count[i]++] =
                    static_cast<unsigned char>(digit);
                next_index[i][digit] = mask_index[mask | (1 << digit)];
            }
        }
    }

    int max_states = (LIMIT + 1) * mask_count;
    seen.assign(max_states, 0);
    parent.resize(max_states);
    queue_ids.resize(max_states);
    last_digit.resize(max_states);
}

u128 least_duodigit_multiple(int n) {
    ++stamp;

    auto state_id = [](int remainder, int mask_id) {
        return remainder * mask_count + mask_id;
    };

    int head = 0;
    int tail = 0;

    for (int digit = 1; digit <= 9; ++digit) {
        int mask_id = mask_index[1 << digit];
        int remainder = digit % n;
        int id = state_id(remainder, mask_id);
        if (seen[id] == stamp) {
            continue;
        }
        seen[id] = stamp;
        parent[id] = -1;
        last_digit[id] = static_cast<unsigned char>(digit);
        if (remainder == 0) {
            return digit;
        }
        queue_ids[tail++] = id;
    }

    while (head < tail) {
        int id = queue_ids[head++];
        int remainder = id / mask_count;
        int mask_id = id - remainder * mask_count;
        int shifted = (remainder * 10) % n;

        for (int i = 0; i < allowed_count[mask_id]; ++i) {
            int digit = allowed_digits[mask_id][i];
            int next_remainder = shifted + digit;
            if (next_remainder >= n) {
                next_remainder %= n;
            }

            int next_mask_id = next_index[mask_id][digit];
            int next_id = state_id(next_remainder, next_mask_id);
            if (seen[next_id] == stamp) {
                continue;
            }

            seen[next_id] = stamp;
            parent[next_id] = id;
            last_digit[next_id] = static_cast<unsigned char>(digit);

            if (next_remainder == 0) {
                unsigned char digits[256];
                int length = 0;
                for (int current = next_id; current != -1; current = parent[current]) {
                    digits[length++] = last_digit[current];
                }

                u128 value = 0;
                for (int j = length - 1; j >= 0; --j) {
                    value = value * 10 + digits[j];
                }
                return value;
            }

            queue_ids[tail++] = next_id;
        }
    }

    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    int limit = LIMIT;
    if (argc > 1) {
        limit = std::stoi(argv[1]);
    }

    prepare_masks();

    u128 total = 0;
    for (int n = 1; n <= limit; ++n) {
        total += least_duodigit_multiple(n);
    }

    std::cout << to_string_u128(total) << '\n';
    return 0;
}
