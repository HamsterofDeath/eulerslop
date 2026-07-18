#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;

constexpr int STEPS = 20;

struct Tiling {
  std::vector<std::vector<int>> neighbours;
  std::vector<int> boundary;

  int add_vertex() {
    neighbours.emplace_back();
    return static_cast<int>(neighbours.size()) - 1;
  }

  void add_edge(int first, int second) {
    neighbours[first].push_back(second);
    neighbours[second].push_back(first);
  }
};

Tiling make_ball(int radius) {
  Tiling tiling;
  const int centre = tiling.add_vertex();
  assert(centre == 0);
  if (radius == 0) {
    return tiling;
  }

  for (int index = 0; index < 7; ++index) {
    const int vertex = tiling.add_vertex();
    tiling.boundary.push_back(vertex);
    tiling.add_edge(centre, vertex);
  }
  for (int index = 0; index < 7; ++index) {
    tiling.add_edge(
        tiling.boundary[index],
        tiling.boundary[(index + 1) % 7]
    );
  }

  for (int layer = 2; layer <= radius; ++layer) {
    const int boundary_size = tiling.boundary.size();
    std::vector<int> old_degrees(boundary_size);
    for (int index = 0; index < boundary_size; ++index) {
      old_degrees[index] =
          tiling.neighbours[tiling.boundary[index]].size();
    }

    // One new vertex completes the triangle outside each old
    // boundary edge.
    std::vector<int> shared(boundary_size);
    for (int index = 0; index < boundary_size; ++index) {
      shared[index] = tiling.add_vertex();
      tiling.add_edge(shared[index], tiling.boundary[index]);
      tiling.add_edge(
          shared[index],
          tiling.boundary[(index + 1) % boundary_size]
      );
    }

    // Fill the remaining fan at each old boundary vertex.  In
    // cyclic order the fan runs shared[i-1], private..., shared[i].
    std::vector<int> next_boundary;
    for (int index = 0; index < boundary_size; ++index) {
      next_boundary.push_back(
          shared[(index + boundary_size - 1) % boundary_size]
      );
      const int private_count = 7 - old_degrees[index] - 2;
      assert(private_count >= 0);
      for (int count = 0; count < private_count; ++count) {
        const int vertex = tiling.add_vertex();
        next_boundary.push_back(vertex);
        tiling.add_edge(vertex, tiling.boundary[index]);
      }
    }
    for (int index = 0;
         index < static_cast<int>(next_boundary.size());
         ++index) {
      tiling.add_edge(
          next_boundary[index],
          next_boundary[(index + 1) % next_boundary.size()]
      );
    }
    for (const int vertex : tiling.boundary) {
      assert(tiling.neighbours[vertex].size() == 7);
    }
    tiling.boundary = std::move(next_boundary);
  }
  return tiling;
}

u64 closed_walks(int steps, int radius = -1) {
  if (radius < 0) {
    radius = steps / 2;
  }
  const Tiling tiling = make_ball(radius);
  std::vector<u64> ways(tiling.neighbours.size());
  ways[0] = 1;

  for (int step = 0; step < steps; ++step) {
    std::vector<u64> next(ways.size());
    for (int vertex = 0;
         vertex < static_cast<int>(ways.size());
         ++vertex) {
      for (const int neighbour : tiling.neighbours[vertex]) {
        next[neighbour] += ways[vertex];
      }
    }
    ways = std::move(next);
  }
  return ways[0];
}

int main(int argc, char** argv) {
  assert(closed_walks(4) == 119);
  const int steps = argc > 1 ? std::stoi(argv[1]) : STEPS;
  const int radius = argc > 2 ? std::stoi(argv[2]) : -1;
  std::cout << closed_walks(steps, radius) << '\n';
}
