#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <optional>
#include <vector>

using u64 = std::uint64_t;
using i64 = std::int64_t;

constexpr int ALPHABET = 10;
constexpr int WORD_LENGTH = 12;
constexpr u64 WORD_MODULUS = 1'000'000'000'000ULL;
constexpr u64 TEN_TO_ELEVEN = 100'000'000'000ULL;
constexpr int ANSWER_MODULUS = 1'234'567'891;

struct Block {
  std::array<unsigned char, WORD_LENGTH> digits{};
  int length = 0;
};

struct ShortBlock {
  u64 key;
  u64 value;
  unsigned char length;
};

struct Record {
  u64 order_key;
  u64 value;

  bool operator<(const Record& other) const {
    return order_key < other.order_key;
  }
};

std::array<unsigned char, WORD_LENGTH> digits_of(
    u64 value
) {
  std::array<unsigned char, WORD_LENGTH> digits{};
  for (int index = WORD_LENGTH - 1; index >= 0; --index) {
    digits[index] = value % 10;
    value /= 10;
  }
  return digits;
}

u64 numeric_value(const Block& block) {
  u64 result = 0;
  for (int index = 0; index < block.length; ++index) {
    result = 10 * result + block.digits[index];
  }
  return result;
}

u64 lexicographic_key(const Block& block) {
  u64 result = 0;
  for (int index = 0; index < WORD_LENGTH; ++index) {
    const int symbol =
        index < block.length ? block.digits[index] + 1 : 0;
    result = 11 * result + symbol;
  }
  return result;
}

bool is_lyndon(const Block& block) {
  if (block.length == 1) {
    return true;
  }
  for (int shift = 1; shift < block.length; ++shift) {
    int comparison = 0;
    for (int index = 0; index < block.length; ++index) {
      const int left = block.digits[index];
      const int right =
          block.digits[(index + shift) % block.length];
      if (left != right) {
        comparison = left < right ? -1 : 1;
        break;
      }
    }
    if (comparison >= 0) {
      return false;
    }
  }
  return true;
}

bool is_full_lyndon(u64 value) {
  u64 rotation = value;
  for (int shift = 1; shift < WORD_LENGTH; ++shift) {
    rotation =
        (rotation % TEN_TO_ELEVEN) * 10
        + rotation / TEN_TO_ELEVEN;
    if (rotation <= value) {
      return false;
    }
  }
  return true;
}

std::vector<ShortBlock> build_short_blocks() {
  const std::array<int, 5> lengths{1, 2, 3, 4, 6};
  std::vector<ShortBlock> blocks;
  blocks.reserve(170'000);

  for (const int length : lengths) {
    u64 count = 1;
    for (int index = 0; index < length; ++index) {
      count *= 10;
    }
    for (u64 value = 0; value < count; ++value) {
      Block block;
      block.length = length;
      u64 remaining = value;
      for (int index = length - 1; index >= 0; --index) {
        block.digits[index] = remaining % 10;
        remaining /= 10;
      }
      if (is_lyndon(block)) {
        blocks.push_back(
            {lexicographic_key(block), value,
             static_cast<unsigned char>(length)}
        );
      }
    }
  }
  std::sort(
      blocks.begin(),
      blocks.end(),
      [](const ShortBlock& left, const ShortBlock& right) {
        return left.key < right.key;
      }
  );
  return blocks;
}

Block block_from_short(const ShortBlock& stored) {
  Block result;
  result.length = stored.length;
  u64 value = stored.value;
  for (int index = result.length - 1; index >= 0; --index) {
    result.digits[index] = value % 10;
    value /= 10;
  }
  return result;
}

Block next_fkm_block(Block current) {
  while (true) {
    std::array<unsigned char, WORD_LENGTH> repeated{};
    for (int index = 0; index < WORD_LENGTH; ++index) {
      repeated[index] =
          current.digits[index % current.length];
    }

    int changed = WORD_LENGTH - 1;
    while (changed >= 0 && repeated[changed] == 9) {
      --changed;
    }
    if (changed < 0) {
      Block first;
      first.length = 1;
      first.digits[0] = 0;
      return first;
    }
    ++repeated[changed];

    Block candidate;
    candidate.length = changed + 1;
    std::copy(
        repeated.begin(),
        repeated.begin() + candidate.length,
        candidate.digits.begin()
    );
    if (WORD_LENGTH % candidate.length == 0) {
      return candidate;
    }
    current = candidate;
  }
}

std::optional<Block> previous_block(
    const Block& current,
    const std::vector<ShortBlock>& short_blocks
) {
  const u64 current_key = lexicographic_key(current);
  std::optional<Block> best;
  u64 best_key = 0;

  const auto short_position = std::lower_bound(
      short_blocks.begin(),
      short_blocks.end(),
      current_key,
      [](const ShortBlock& block, u64 key) {
        return block.key < key;
      }
  );
  if (short_position != short_blocks.begin()) {
    best = block_from_short(*std::prev(short_position));
    best_key = lexicographic_key(*best);
  }

  std::optional<u64> full_upper;
  if (current.length == WORD_LENGTH) {
    const u64 value = numeric_value(current);
    if (value != 0) {
      full_upper = value - 1;
    }
  } else {
    int changed = current.length - 1;
    while (changed >= 0 && current.digits[changed] == 0) {
      --changed;
    }
    if (changed >= 0) {
      u64 upper = 0;
      for (int index = 0; index < changed; ++index) {
        upper = 10 * upper + current.digits[index];
      }
      upper = 10 * upper + current.digits[changed] - 1;
      for (
          int index = changed + 1;
          index < WORD_LENGTH;
          ++index
      ) {
        upper = 10 * upper + 9;
      }
      full_upper = upper;
    }
  }

  if (full_upper.has_value()) {
    u64 candidate_value = *full_upper;
    while (true) {
      if (is_full_lyndon(candidate_value)) {
        Block candidate;
        candidate.length = WORD_LENGTH;
        candidate.digits = digits_of(candidate_value);
        const u64 key = lexicographic_key(candidate);
        if (!best.has_value() || key > best_key) {
          best = candidate;
        }
        break;
      }
      if (candidate_value == 0) {
        break;
      }
      --candidate_value;
    }
  }
  return best;
}

std::optional<int> window_offset(
    const Block& owner,
    u64 target
) {
  std::vector<unsigned char> sequence;
  sequence.reserve(owner.length + WORD_LENGTH);
  for (int index = 0; index < owner.length; ++index) {
    sequence.push_back(owner.digits[index]);
  }

  Block next = owner;
  while (
      static_cast<int>(sequence.size())
      < owner.length + WORD_LENGTH - 1
  ) {
    next = next_fkm_block(next);
    for (int index = 0; index < next.length; ++index) {
      sequence.push_back(next.digits[index]);
    }
  }

  u64 window = 0;
  for (int index = 0; index < WORD_LENGTH; ++index) {
    window = 10 * window + sequence[index];
  }
  for (int offset = 0; offset < owner.length; ++offset) {
    if (window == target) {
      return offset;
    }
    if (offset + 1 < owner.length) {
      window =
          (window % TEN_TO_ELEVEN) * 10
          + sequence[offset + WORD_LENGTH];
    }
  }
  return std::nullopt;
}

Block minimal_rotation_block(u64 value) {
  u64 minimum = value;
  u64 rotation = value;
  for (int shift = 1; shift < WORD_LENGTH; ++shift) {
    rotation =
        (rotation % TEN_TO_ELEVEN) * 10
        + rotation / TEN_TO_ELEVEN;
    minimum = std::min(minimum, rotation);
  }

  const auto digits = digits_of(minimum);
  const std::array<int, 6> divisors{1, 2, 3, 4, 6, 12};
  for (const int period : divisors) {
    bool periodic = true;
    for (int index = period; index < WORD_LENGTH; ++index) {
      if (digits[index] != digits[index % period]) {
        periodic = false;
        break;
      }
    }
    if (periodic) {
      Block result;
      result.length = period;
      std::copy(
          digits.begin(),
          digits.begin() + period,
          result.digits.begin()
      );
      return result;
    }
  }
  return {};
}

u64 occurrence_order_key(
    u64 word,
    const std::vector<ShortBlock>& short_blocks
) {
  Block candidate = minimal_rotation_block(word);
  const std::optional<int> minimal_offset =
      window_offset(candidate, word);
  if (minimal_offset.has_value()) {
    return 12 * lexicographic_key(candidate)
        + *minimal_offset;
  }

  // If the window crosses a carry between adjacent full-length
  // Lyndon blocks, its owner can be reconstructed directly: the
  // known prefix of the next block is one greater than the missing
  // prefix of the owner.
  const auto word_digits = digits_of(word);
  for (int suffix_length = 1;
       suffix_length < WORD_LENGTH;
       ++suffix_length) {
    const int prefix_length = WORD_LENGTH - suffix_length;
    for (int changed = 0; changed < prefix_length; ++changed) {
      const int next_digit =
          word_digits[suffix_length + changed];
      if (next_digit == 0) {
        continue;
      }

      Block owner;
      owner.length = WORD_LENGTH;
      for (int index = 0; index < changed; ++index) {
        owner.digits[index] =
            word_digits[suffix_length + index];
      }
      owner.digits[changed] = next_digit - 1;
      for (
          int index = changed + 1;
          index < prefix_length;
          ++index
      ) {
        owner.digits[index] = 9;
      }
      for (
          int index = 0;
          index < suffix_length;
          ++index
      ) {
        owner.digits[prefix_length + index] =
            word_digits[index];
      }
      if (!is_full_lyndon(numeric_value(owner))) {
        continue;
      }
      const std::optional<int> offset =
          window_offset(owner, word);
      if (offset.has_value()) {
        return 12 * lexicographic_key(owner) + *offset;
      }
    }
  }

  for (int attempt = 1; attempt <= 256; ++attempt) {
    const std::optional<Block> previous =
        previous_block(candidate, short_blocks);
    if (!previous.has_value()) {
      break;
    }
    candidate = *previous;
    const std::optional<int> offset =
        window_offset(candidate, word);
    if (offset.has_value()) {
      return 12 * lexicographic_key(candidate) + *offset;
    }
  }

  // The only windows whose owner lies after their minimal
  // rotation cross the cyclic join from the final block to 0.
  const auto digits = digits_of(word);
  int nines = 0;
  while (nines < WORD_LENGTH && digits[nines] == 9) {
    ++nines;
  }
  bool zeros_after = nines > 0;
  for (int index = nines; index < WORD_LENGTH; ++index) {
    zeros_after &= digits[index] == 0;
  }
  if (zeros_after && nines < WORD_LENGTH) {
    if (nines == 1) {
      Block final;
      final.length = 1;
      final.digits[0] = 9;
      return 12 * lexicographic_key(final);
    }
    Block penultimate;
    penultimate.length = WORD_LENGTH;
    penultimate.digits[0] = 8;
    for (int index = 1; index < WORD_LENGTH; ++index) {
      penultimate.digits[index] = 9;
    }
    const int offset = WORD_LENGTH - nines + 1;
    return 12 * lexicographic_key(penultimate) + offset;
  }

  std::cerr << "could not decode word " << word << '\n';
  std::exit(1);
}

int sampled_order_sum(int count) {
  const std::vector<ShortBlock> short_blocks =
      build_short_blocks();
  std::vector<Record> records;
  records.reserve(count);

  u64 value = 0;
  for (int index = 0; index < count; ++index) {
    value = (
        920'461ULL * value + 800'217'387'569ULL
    ) % WORD_MODULUS;
    records.push_back(
        {
            occurrence_order_key(value, short_blocks),
            value,
        }
    );
  }
  std::sort(records.begin(), records.end());

  i64 result = 0;
  for (int index = 0; index < count; ++index) {
    if (
        index > 0
        && records[index].order_key
            == records[index - 1].order_key
    ) {
      std::cerr << "duplicate decoded occurrence\n";
      std::exit(1);
    }
    result +=
        static_cast<i64>((index + 1LL) % ANSWER_MODULUS)
        * (records[index].value % ANSWER_MODULUS)
        % ANSWER_MODULUS;
    result %= ANSWER_MODULUS;
  }
  return static_cast<int>(result);
}

int main(int argc, char** argv) {
  const int count =
      argc > 1 ? std::stoi(argv[1]) : 10'000'000;

  if (
      sampled_order_sum(2) != 2'194'210'461'325ULL
          % ANSWER_MODULUS
      || sampled_order_sum(10)
          != 32'698'850'376'317ULL % ANSWER_MODULUS
  ) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << sampled_order_sum(count) << '\n';
}
