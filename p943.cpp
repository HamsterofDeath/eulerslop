#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <vector>

using u64 = std::uint64_t;

constexpr u64 TARGET_LENGTH = 22'332'223'332'233ULL;
constexpr u64 OUTPUT_MODULUS = 2'233'222'333ULL;

class RunWord {
 public:
  RunWord(int first_symbol, int second_symbol, u64 modulus)
      : symbols_{first_symbol, second_symbol}, modulus_(modulus) {
    nodes_.reserve(4096);
    interned_.reserve(4096);
    make_leaf(first_symbol);
    make_leaf(second_symbol);
  }

  u64 prefix_sum(u64 wanted) {
    int root = 0;
    while (nodes_[root].length < wanted) {
      root = expand(root, 0);
    }
    return prefix(root, wanted);
  }

 private:
  enum class Type : std::uint8_t { leaf, concat, repeat };

  struct Node {
    u64 length;
    u64 sum;
    int first;
    int second;
    std::array<int, 2> expansion;
    Type type;
  };

  std::array<int, 2> symbols_;
  u64 modulus_;
  std::vector<Node> nodes_;
  std::unordered_map<u64, int> interned_;

  int make_leaf(int symbol) {
    const int id = static_cast<int>(nodes_.size());
    nodes_.push_back(
        {1, static_cast<u64>(symbol) % modulus_, symbol, 0, {-1, -1},
         Type::leaf}
    );
    return id;
  }

  int make_concat(int left, int right) {
    const u64 key =
        (static_cast<u64>(static_cast<std::uint32_t>(left)) << 32)
        | static_cast<std::uint32_t>(right);
    auto found = interned_.find(key);
    if (found != interned_.end()) {
      return found->second;
    }

    const int id = static_cast<int>(nodes_.size());
    nodes_.push_back(
        {nodes_[left].length + nodes_[right].length,
         (nodes_[left].sum + nodes_[right].sum) % modulus_,
         left, right, {-1, -1}, Type::concat}
    );
    interned_.emplace(key, id);
    return id;
  }

  int make_repeat(int child, int count) {
    if (count == 1) {
      return child;
    }
    const u64 key =
        (u64{1} << 63)
        | (static_cast<u64>(static_cast<std::uint32_t>(child)) << 16)
        | static_cast<std::uint16_t>(count);
    auto found = interned_.find(key);
    if (found != interned_.end()) {
      return found->second;
    }

    const int id = static_cast<int>(nodes_.size());
    nodes_.push_back(
        {nodes_[child].length * static_cast<u64>(count),
         nodes_[child].sum * static_cast<u64>(count) % modulus_,
         child, count, {-1, -1}, Type::repeat}
    );
    interned_.emplace(key, id);
    return id;
  }

  int expand(int id, int phase) {
    const int cached = nodes_[id].expansion[phase];
    if (cached >= 0) {
      return cached;
    }

    // Copy the fields: recursive calls can reallocate nodes_.
    const Type type = nodes_[id].type;
    const int first = nodes_[id].first;
    const int second = nodes_[id].second;
    int result;

    if (type == Type::leaf) {
      result = make_repeat(phase, first);
    } else if (type == Type::concat) {
      const int expanded_left = expand(first, phase);
      const int next_phase =
          phase ^ static_cast<int>(nodes_[first].length & 1);
      const int expanded_right = expand(second, next_phase);
      result = make_concat(expanded_left, expanded_right);
    } else {
      const int child = first;
      const int count = second;
      const int expanded_first = expand(child, phase);
      if ((nodes_[child].length & 1) == 0) {
        result = make_repeat(expanded_first, count);
      } else {
        const int expanded_second = expand(child, phase ^ 1);
        const int pair =
            make_concat(expanded_first, expanded_second);
        result = make_repeat(pair, count / 2);
        if (count & 1) {
          result = make_concat(result, expanded_first);
        }
      }
    }

    nodes_[id].expansion[phase] = result;
    return result;
  }

  u64 prefix(int id, u64 wanted) const {
    if (wanted == 0) {
      return 0;
    }
    const Node& node = nodes_[id];
    if (wanted == node.length) {
      return node.sum;
    }
    if (node.type == Type::leaf) {
      return node.sum;
    }
    if (node.type == Type::concat) {
      const Node& left = nodes_[node.first];
      if (wanted <= left.length) {
        return prefix(node.first, wanted);
      }
      return (left.sum + prefix(node.second, wanted - left.length))
             % modulus_;
    }

    const Node& child = nodes_[node.first];
    const u64 complete = wanted / child.length;
    const u64 remainder = wanted % child.length;
    return (
        complete * child.sum + prefix(node.first, remainder)
    ) % modulus_;
  }
};

u64 T(int a, int b, u64 length, u64 modulus) {
  return RunWord(a, b, modulus).prefix_sum(length);
}

int main() {
  if (
      T(2, 3, 10, OUTPUT_MODULUS) != 25
      || T(4, 2, 10'000, OUTPUT_MODULUS) != 30'004
      || T(5, 8, 1'000'000, OUTPUT_MODULUS) != 6'499'871
  ) {
    throw std::runtime_error("sample self-check failed");
  }

  u64 answer = 0;
  for (int a = 2; a <= 223; ++a) {
    for (int b = 2; b <= 223; ++b) {
      if (a != b) {
        answer += T(a, b, TARGET_LENGTH, OUTPUT_MODULUS);
        answer %= OUTPUT_MODULUS;
      }
    }
  }
  std::cout << answer << '\n';
}
