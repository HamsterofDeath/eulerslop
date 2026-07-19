#include <algorithm>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <thread>
#include <utility>
#include <vector>

using i64 = std::int64_t;

bool prerequisite_moves_die_out(int c, int d, i64 target_moves) {
  const int state_size = c + d;
  std::vector<i64> state(state_size);
  state.back() = target_moves;

  while (true) {
    i64 minimum = std::numeric_limits<i64>::max();
    i64 maximum = 0;
    for (int index = 0; index < state_size; ++index) {
      const int other = (index + c) % state_size;
      state[index] = (state[index] + state[other]) / 2;
      minimum = std::min(minimum, state[index]);
      maximum = std::max(maximum, state[index]);
    }

    if (maximum == 0) {
      return true;
    }
    if (minimum > 0) {
      return false;
    }
  }
}

i64 maximum_tokens(int c, int d) {
  const int common = std::gcd(c, d);
  c /= common;
  d /= common;

  i64 dying = 0;
  i64 persistent = 1;
  while (prerequisite_moves_die_out(c, d, persistent)) {
    dying = persistent;
    persistent *= 2;
  }

  while (persistent - dying > 1) {
    const i64 middle = (dying + persistent) / 2;
    if (prerequisite_moves_die_out(c, d, middle)) {
      dying = middle;
    } else {
      persistent = middle;
    }
  }
  return 1 + 2 * dying;
}

struct Job {
  int c;
  int d;
  int multiplicity;
};

i64 sum_games(int limit) {
  std::map<std::pair<int, int>, int> multiplicities;
  for (int c = 1; c <= limit; ++c) {
    for (int d = 1; d <= limit; ++d) {
      const int common = std::gcd(c, d);
      ++multiplicities[{c / common, d / common}];
    }
  }

  std::vector<Job> jobs;
  jobs.reserve(multiplicities.size());
  for (const auto& [pair, multiplicity] : multiplicities) {
    jobs.push_back({pair.first, pair.second, multiplicity});
  }

  std::atomic<std::size_t> next_job{0};
  std::atomic<i64> answer{0};
  const unsigned int worker_count = std::max(
      1U,
      std::min<unsigned int>(
          std::thread::hardware_concurrency(),
          static_cast<unsigned int>(jobs.size())));

  std::vector<std::thread> workers;
  workers.reserve(worker_count);
  for (unsigned int worker = 0; worker < worker_count; ++worker) {
    workers.emplace_back([&]() {
      i64 subtotal = 0;
      while (true) {
        const std::size_t index = next_job.fetch_add(1);
        if (index >= jobs.size()) {
          break;
        }
        const Job& job = jobs[index];
        subtotal +=
            maximum_tokens(job.c, job.d) * job.multiplicity;
      }
      answer.fetch_add(subtotal);
    });
  }
  for (std::thread& worker : workers) {
    worker.join();
  }
  return answer.load();
}

int main(int argc, char** argv) {
  assert(maximum_tokens(2, 1) == 7);
  assert(maximum_tokens(1, 2) == 7);
  assert(maximum_tokens(3, 1) == 11);
  assert(maximum_tokens(2, 2) == 3);
  assert(maximum_tokens(1, 3) == 15);

  const int limit = argc > 1 ? std::stoi(argv[1]) : 160;
  std::cout << sum_games(limit) << '\n';
}
