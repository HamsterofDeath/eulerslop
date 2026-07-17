#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using i64 = std::int64_t;

namespace {

constexpr i64 MODULUS = 1'000'000'007;
constexpr double ROOT_THREE = 1.7320508075688772935;
constexpr double EPSILON = 1e-8;

struct Point {
    int a;
    int b;
    int c;
    int d;

    bool operator==(const Point& other) const {
        return a == other.a && b == other.b
            && c == other.c && d == other.d;
    }

    bool operator<(const Point& other) const {
        return std::array<int, 4>{a, b, c, d}
            < std::array<int, 4>{other.a, other.b, other.c, other.d};
    }
};

struct PointHash {
    std::size_t operator()(const Point& point) const {
        std::size_t result = 0xcbf29ce484222325ULL;
        for (int value : {point.a, point.b, point.c, point.d}) {
            result ^= static_cast<std::uint32_t>(value);
            result *= 0x100000001b3ULL;
        }
        return result;
    }
};

Point operator+(const Point& first, const Point& second) {
    return {
        first.a + second.a,
        first.b + second.b,
        first.c + second.c,
        first.d + second.d,
    };
}

Point operator-(const Point& first, const Point& second) {
    return {
        first.a - second.a,
        first.b - second.b,
        first.c - second.c,
        first.d - second.d,
    };
}

const std::array<Point, 12> DIRECTIONS{{
    {2, 0, 0, 0},
    {0, 1, 1, 0},
    {1, 0, 0, 1},
    {0, 0, 2, 0},
    {-1, 0, 0, 1},
    {0, -1, 1, 0},
    {-2, 0, 0, 0},
    {0, -1, -1, 0},
    {-1, 0, 0, -1},
    {0, 0, -2, 0},
    {1, 0, 0, -1},
    {0, 1, -1, 0},
}};

Point rotate_thirty(const Point& point) {
    const std::array<int, 4> numerators{{
        3 * point.b - point.c,
        point.a - point.d,
        point.a + 3 * point.d,
        point.b + point.c,
    }};
    for (int value : numerators) {
        assert(value % 2 == 0);
    }
    return {
        numerators[0] / 2,
        numerators[1] / 2,
        numerators[2] / 2,
        numerators[3] / 2,
    };
}

Point rotate_sixty(const Point& point) {
    return rotate_thirty(rotate_thirty(point));
}

std::pair<double, double> xy(const Point& point) {
    return {
        (point.a + point.b * ROOT_THREE) / 2,
        (point.c + point.d * ROOT_THREE) / 2,
    };
}

struct Edge {
    Point first;
    Point second;

    bool operator==(const Edge& other) const {
        return first == other.first && second == other.second;
    }

    bool operator<(const Edge& other) const {
        if (first < other.first) {
            return true;
        }
        if (other.first < first) {
            return false;
        }
        return second < other.second;
    }
};

Edge reversed(const Edge& edge) {
    return {edge.second, edge.first};
}

struct Tile {
    int sides;
    std::vector<Point> vertices;

    bool operator==(const Tile& other) const {
        return sides == other.sides && vertices == other.vertices;
    }

    bool operator<(const Tile& other) const {
        if (sides != other.sides) {
            return sides < other.sides;
        }
        return vertices < other.vertices;
    }
};

using Boundary = std::set<Edge>;
using Tiles = std::set<Tile>;

double cross(
    const Point& first,
    const Point& second,
    const Point& third
) {
    const auto [ax, ay] = xy(first);
    const auto [bx, by] = xy(second);
    const auto [cx, cy] = xy(third);
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax);
}

bool segments_intersect_badly(
    const Point& first,
    const Point& second,
    const Point& third,
    const Point& fourth
) {
    const auto a = xy(first);
    const auto b = xy(second);
    const auto c = xy(third);
    const auto d = xy(fourth);
    const auto determinant = [](const auto& p, const auto& q, const auto& r) {
        return (q.first - p.first) * (r.second - p.second)
            - (q.second - p.second) * (r.first - p.first);
    };
    const std::array<double, 4> values{{
        determinant(a, b, c),
        determinant(a, b, d),
        determinant(c, d, a),
        determinant(c, d, b),
    }};
    if (values[0] * values[1] < -EPSILON
        && values[2] * values[3] < -EPSILON) {
        return true;
    }

    const auto interior_on_segment = [&](const auto& p, const auto& q, const auto& r) {
        return std::abs(determinant(p, q, r)) < EPSILON
            && (
                (
                    std::min(p.first, q.first) + EPSILON < r.first
                    && r.first < std::max(p.first, q.first) - EPSILON
                )
                || (
                    std::min(p.second, q.second) + EPSILON < r.second
                    && r.second < std::max(p.second, q.second) - EPSILON
                )
            );
    };
    return interior_on_segment(a, b, c)
        || interior_on_segment(a, b, d)
        || interior_on_segment(c, d, a)
        || interior_on_segment(c, d, b);
}

int winding_number(
    const std::pair<double, double>& point,
    const Boundary& boundary
) {
    const auto [x, y] = point;
    int winding = 0;
    for (const auto& edge : boundary) {
        const auto [ax, ay] = xy(edge.first);
        const auto [bx, by] = xy(edge.second);
        const double side = (
            (bx - ax) * (y - ay) - (by - ay) * (x - ax)
        );
        if (ay <= y && y < by && side > EPSILON) {
            ++winding;
        } else if (by <= y && y < ay && side < -EPSILON) {
            --winding;
        }
    }
    return winding;
}

std::vector<Point> polygon(const Edge& edge, int sides) {
    int direction_index = -1;
    const Point delta = edge.second - edge.first;
    for (int index = 0; index < 12; ++index) {
        if (DIRECTIONS[index] == delta) {
            direction_index = index;
            break;
        }
    }
    assert(direction_index >= 0);

    const int step = 12 / sides;
    Point point = edge.first;
    std::vector<Point> vertices{point};
    for (int edge_index = 0; edge_index < sides; ++edge_index) {
        point = point + DIRECTIONS[
            (direction_index + edge_index * step) % 12
        ];
        if (edge_index + 1 < sides) {
            vertices.push_back(point);
        }
    }
    assert(point == edge.first);
    return vertices;
}

Tile make_tile(int sides, std::vector<Point> vertices) {
    std::sort(vertices.begin(), vertices.end());
    return {sides, std::move(vertices)};
}

std::vector<Edge> tile_edges(const std::vector<Point>& vertices) {
    std::vector<Edge> result;
    for (int index = 0; index < static_cast<int>(vertices.size()); ++index) {
        result.push_back({
            vertices[index],
            vertices[(index + 1) % vertices.size()],
        });
    }
    return result;
}

bool place_tile(
    const Boundary& boundary,
    const std::vector<Point>& vertices,
    Boundary& next_boundary
) {
    const int sides = static_cast<int>(vertices.size());
    double center_x = 0;
    double center_y = 0;
    for (const Point& vertex : vertices) {
        const auto [x, y] = xy(vertex);
        center_x += x;
        center_y += y;
    }
    center_x /= sides;
    center_y /= sides;
    if (winding_number({center_x, center_y}, boundary) <= 0) {
        return false;
    }

    const auto candidate_edges = tile_edges(vertices);
    for (const Edge& candidate : candidate_edges) {
        for (const Edge& existing : boundary) {
            if (candidate == existing) {
                continue;
            }
            if (segments_intersect_badly(
                candidate.first,
                candidate.second,
                existing.first,
                existing.second
            )) {
                return false;
            }
        }
    }

    std::set<Point> candidate_vertices(
        vertices.begin(), vertices.end()
    );
    std::set<Point> boundary_vertices;
    for (const Edge& edge : boundary) {
        boundary_vertices.insert(edge.first);
        boundary_vertices.insert(edge.second);
    }
    for (const Point& point : boundary_vertices) {
        if (candidate_vertices.count(point)) {
            continue;
        }
        bool strictly_inside = true;
        for (int index = 0; index < sides; ++index) {
            if (cross(
                vertices[index],
                vertices[(index + 1) % sides],
                point
            ) <= EPSILON) {
                strictly_inside = false;
                break;
            }
        }
        if (strictly_inside) {
            return false;
        }
    }

    next_boundary = boundary;
    for (const Edge& edge : candidate_edges) {
        if (next_boundary.erase(edge)) {
            continue;
        }
        if (next_boundary.count(reversed(edge))) {
            return false;
        }
        next_boundary.insert(reversed(edge));
    }
    return true;
}

std::vector<Edge> centered_boundary(int first_length, int second_length) {
    Point point{
        -first_length,
        0,
        -2 * second_length,
        -first_length,
    };
    std::vector<Edge> result;
    for (int direction_index = 0; direction_index < 12; ++direction_index) {
        const int length = (
            direction_index % 2 == 0 ? first_length : second_length
        );
        for (int step = 0; step < length; ++step) {
            const Point next_point = point + DIRECTIONS[direction_index];
            result.push_back({point, next_point});
            point = next_point;
        }
    }
    return result;
}

void toggle_edge(Boundary& boundary, const Edge& edge) {
    if (!boundary.erase(reversed(edge))) {
        boundary.insert(edge);
    }
}

Boundary corona_boundary(
    int first_length,
    int second_length,
    bool increment_first
) {
    Boundary result;
    const int outer_first = first_length + (increment_first ? 1 : 0);
    const int outer_second = second_length + (increment_first ? 0 : 1);
    for (const Edge& edge : centered_boundary(outer_first, outer_second)) {
        toggle_edge(result, edge);
    }
    for (const Edge& edge : centered_boundary(first_length, second_length)) {
        toggle_edge(result, reversed(edge));
    }
    return result;
}

std::vector<Point> rotate_polygon_sixty(
    const std::vector<Point>& vertices
) {
    std::vector<Point> result;
    result.reserve(vertices.size());
    for (const Point& point : vertices) {
        result.push_back(rotate_sixty(point));
    }
    return result;
}

bool find_symmetric_tiling(
    const Boundary& boundary,
    Tiles& result,
    std::set<Boundary>& failed
) {
    if (boundary.empty()) {
        result.clear();
        return true;
    }
    if (failed.count(boundary)) {
        return false;
    }

    const Edge edge = *boundary.begin();
    for (int sides : {3, 4}) {
        Boundary next_boundary = boundary;
        std::vector<Point> vertices = polygon(edge, sides);
        Tiles orbit;
        bool valid = true;
        for (int rotation = 0; rotation < 6; ++rotation) {
            const Tile tile = make_tile(sides, vertices);
            if (!orbit.count(tile)) {
                Boundary placed;
                if (!place_tile(next_boundary, vertices, placed)) {
                    valid = false;
                    break;
                }
                next_boundary = std::move(placed);
                orbit.insert(tile);
            }
            vertices = rotate_polygon_sixty(vertices);
        }
        if (!valid) {
            continue;
        }
        Tiles suffix;
        if (find_symmetric_tiling(next_boundary, suffix, failed)) {
            result = std::move(orbit);
            result.insert(suffix.begin(), suffix.end());
            return true;
        }
    }
    failed.insert(boundary);
    return false;
}

struct CoronaKey {
    int first;
    int second;
    bool increment_first;

    bool operator<(const CoronaKey& other) const {
        return std::array<int, 3>{
            first, second, increment_first
        } < std::array<int, 3>{
            other.first, other.second, other.increment_first
        };
    }
};

std::map<CoronaKey, Tiles> corona_cache;

const Tiles& corona(int first, int second, bool increment_first) {
    const CoronaKey key{first, second, increment_first};
    const auto found = corona_cache.find(key);
    if (found != corona_cache.end()) {
        return found->second;
    }
    Tiles result;
    std::set<Boundary> failed;
    assert(find_symmetric_tiling(
        corona_boundary(first, second, increment_first),
        result,
        failed
    ));
    return corona_cache.emplace(key, std::move(result)).first->second;
}

i64 modular_power(i64 base, i64 exponent) {
    i64 result = 1;
    while (exponent) {
        if (exponent & 1) {
            result = result * base % MODULUS;
        }
        base = base * base % MODULUS;
        exponent >>= 1;
    }
    return result;
}

using Coordinate = std::pair<int, int>;
using Signature = std::vector<Coordinate>;

Signature normalize_coordinates(const std::set<Coordinate>& coordinates) {
    const Coordinate origin = *coordinates.begin();
    Signature result;
    result.reserve(coordinates.size());
    for (const auto& [u, v] : coordinates) {
        result.push_back({u - origin.first, v - origin.second});
    }
    return result;
}

std::set<Coordinate> rotate_coordinates(
    const std::set<Coordinate>& coordinates
) {
    std::set<Coordinate> result;
    for (const auto& [u, v] : coordinates) {
        result.insert({-v, u + v});
    }
    return result;
}

Signature canonical_coordinates(std::set<Coordinate> coordinates) {
    Signature best;
    bool initialized = false;
    for (int rotation = 0; rotation < 6; ++rotation) {
        for (bool reflected : {false, true}) {
            std::set<Coordinate> transformed;
            if (reflected) {
                for (const auto& [u, v] : coordinates) {
                    transformed.insert({u + v, -v});
                }
            } else {
                transformed = coordinates;
            }
            const Signature normalized = normalize_coordinates(transformed);
            if (!initialized || normalized < best) {
                best = normalized;
                initialized = true;
            }
        }
        coordinates = rotate_coordinates(coordinates);
    }
    return best;
}

Signature component_signature(
    const std::unordered_set<Point, PointHash>& component
) {
    if (component.size() == 1) {
        return {{0, 0}};
    }

    const Point first = *component.begin();
    int parity = -1;
    for (int index = 0; index < 12; ++index) {
        if (component.count(first + DIRECTIONS[index])) {
            parity = index % 2;
            break;
        }
    }
    assert(parity >= 0);

    const std::array<Coordinate, 6> steps{{
        {1, 0},
        {0, 1},
        {-1, 1},
        {-1, 0},
        {0, -1},
        {1, -1},
    }};
    std::unordered_map<Point, Coordinate, PointHash> coordinates;
    coordinates[first] = {0, 0};
    std::vector<Point> stack{first};
    while (!stack.empty()) {
        const Point point = stack.back();
        stack.pop_back();
        const auto [u, v] = coordinates.at(point);
        for (int direction_index = 0; direction_index < 12; ++direction_index) {
            const Point neighbor = point + DIRECTIONS[direction_index];
            if (!component.count(neighbor)) {
                continue;
            }
            const int offset = (
                direction_index - parity + 12
            ) % 12;
            if (offset % 2) {
                continue;
            }
            const auto [du, dv] = steps[offset / 2];
            const Coordinate next{u + du, v + dv};
            const auto found = coordinates.find(neighbor);
            if (found == coordinates.end()) {
                coordinates[neighbor] = next;
                stack.push_back(neighbor);
            } else {
                assert(found->second == next);
            }
        }
    }
    assert(coordinates.size() == component.size());
    std::set<Coordinate> coordinate_set;
    for (const auto& [point, coordinate] : coordinates) {
        coordinate_set.insert(coordinate);
    }
    return canonical_coordinates(std::move(coordinate_set));
}

std::map<Signature, i64> independent_cache;

i64 lattice_independent_sets(const Signature& signature) {
    const auto found = independent_cache.find(signature);
    if (found != independent_cache.end()) {
        return found->second;
    }
    if (signature.size() == 1) {
        independent_cache[signature] = 2;
        return 2;
    }

    std::set<Coordinate> coordinates(
        signature.begin(), signature.end()
    );
    std::set<Coordinate> best_coordinates;
    int best_width = 1'000'000;
    for (int rotation = 0; rotation < 3; ++rotation) {
        int minimum_v = 1'000'000;
        int maximum_v = -1'000'000;
        for (const auto& [u, v] : coordinates) {
            minimum_v = std::min(minimum_v, v);
            maximum_v = std::max(maximum_v, v);
        }
        const int width = maximum_v - minimum_v + 1;
        if (width < best_width) {
            best_width = width;
            best_coordinates = coordinates;
        }
        coordinates = rotate_coordinates(coordinates);
    }
    coordinates = std::move(best_coordinates);
    assert(best_width < 31);

    int minimum_u = 1'000'000;
    int maximum_u = -1'000'000;
    int minimum_v = 1'000'000;
    for (const auto& [u, v] : coordinates) {
        minimum_u = std::min(minimum_u, u);
        maximum_u = std::max(maximum_u, u);
        minimum_v = std::min(minimum_v, v);
    }
    std::vector<std::uint32_t> row_availability(
        maximum_u - minimum_u + 1
    );
    for (const auto& [u, v] : coordinates) {
        row_availability[u - minimum_u] |= (
            1U << (v - minimum_v)
        );
    }

    const std::uint32_t state_count = 1U << best_width;
    std::vector<i64> values(state_count);
    values[0] = 1;
    for (std::uint32_t available : row_availability) {
        std::vector<i64> subset_sums = values;
        for (std::uint32_t bit = 1; bit < state_count; bit <<= 1) {
            for (std::uint32_t base = 0; base < state_count; base += 2 * bit) {
                for (std::uint32_t offset = 0; offset < bit; ++offset) {
                    i64& value = subset_sums[base + bit + offset];
                    value += subset_sums[base + offset];
                    if (value >= MODULUS) {
                        value -= MODULUS;
                    }
                }
            }
        }

        std::vector<i64> next_values(state_count);
        std::uint32_t mask = available;
        while (true) {
            if ((mask & (mask << 1)) == 0) {
                const std::uint32_t forbidden = mask | (mask << 1);
                const std::uint32_t allowed_previous = (
                    state_count - 1
                ) & ~forbidden;
                next_values[mask] = subset_sums[allowed_previous];
            }
            if (mask == 0) {
                break;
            }
            mask = (mask - 1) & available;
        }
        values = std::move(next_values);
    }
    i64 result = 0;
    for (i64 value : values) {
        result += value;
        if (result >= MODULUS) {
            result -= MODULUS;
        }
    }
    independent_cache[signature] = result;
    return result;
}

std::unordered_set<Point, PointHash> rotate_component_sixty(
    const std::unordered_set<Point, PointHash>& component
) {
    std::unordered_set<Point, PointHash> result;
    result.reserve(component.size());
    for (const Point& point : component) {
        result.insert(rotate_sixty(point));
    }
    return result;
}

std::map<int, i64> central_values;

i64 all_independent_sets(
    const std::unordered_set<Point, PointHash>& candidates
) {
    std::unordered_set<Point, PointHash> unseen = candidates;
    i64 result = 1;
    while (!unseen.empty()) {
        const Point first = *unseen.begin();
        unseen.erase(first);
        std::unordered_set<Point, PointHash> component{first};
        std::vector<Point> stack{first};
        while (!stack.empty()) {
            const Point point = stack.back();
            stack.pop_back();
            for (const Point& direction : DIRECTIONS) {
                const Point neighbor = point + direction;
                if (unseen.erase(neighbor)) {
                    component.insert(neighbor);
                    stack.push_back(neighbor);
                }
            }
        }

        i64 value;
        int orbit_size;
        if (component.count({0, 0, 0, 0})) {
            const int size = static_cast<int>(component.size());
            const auto found = central_values.find(size);
            if (found == central_values.end()) {
                value = lattice_independent_sets(
                    component_signature(component)
                );
                central_values[size] = value;
            } else {
                value = found->second;
            }
            orbit_size = 1;
        } else {
            value = lattice_independent_sets(
                component_signature(component)
            );
            orbit_size = 1;
            auto rotated = component;
            for (int rotation = 0; rotation < 5; ++rotation) {
                rotated = rotate_component_sixty(rotated);
                bool removed = false;
                for (const Point& point : rotated) {
                    removed = unseen.erase(point) || removed;
                }
                if (removed) {
                    ++orbit_size;
                }
            }
            assert(orbit_size == 6);
        }
        result = result * modular_power(value, orbit_size) % MODULUS;
    }
    return result;
}

struct Incidence {
    int triangles = 0;
    int squares = 0;
    int central = 0;
};

class Counter {
public:
    explicit Counter(int side_length) : side_length_(side_length) {
        for (const Tile& tile : corona(0, 0, true)) {
            central_tiles_.insert(tile);
        }
        for (const Tile& tile : corona(1, 0, false)) {
            central_tiles_.insert(tile);
        }
        for (const Tile& tile : corona(0, 0, false)) {
            central_tiles_.insert(tile);
        }
        for (const Tile& tile : corona(0, 1, true)) {
            central_tiles_.insert(tile);
        }
    }

    i64 run() {
        const std::uint32_t root = (
            (1U << side_length_) - 1
        );
        int first = 0;
        int second = 0;
        for (int index = 0; index < 2 * side_length_; ++index) {
            const bool increment_first = index < side_length_;
            update_tiles(corona(first, second, increment_first), 1);
            if (increment_first) {
                ++first;
            } else {
                ++second;
            }
        }
        visit(root);
        assert(visited_ == binomial(2 * side_length_, side_length_));
        const i64 inverse_two = (MODULUS + 1) / 2;
        return (
            without_dodecagon_
            + refined_dodecagon_ * inverse_two
        ) % MODULUS;
    }

private:
    int side_length_;
    Tiles central_tiles_;
    std::unordered_map<Point, Incidence, PointHash> incidence_;
    std::unordered_set<Point, PointHash> candidates_;
    i64 without_dodecagon_ = 0;
    i64 refined_dodecagon_ = 0;
    i64 visited_ = 0;

    static i64 binomial(int top, int bottom) {
        i64 result = 1;
        for (int value = 1; value <= bottom; ++value) {
            result = result * (top - bottom + value) / value;
        }
        return result;
    }

    void update_tiles(const Tiles& tiles, int change) {
        for (const Tile& tile : tiles) {
            const bool central = central_tiles_.count(tile);
            for (const Point& vertex : tile.vertices) {
                auto [iterator, inserted] = incidence_.try_emplace(vertex);
                Incidence& counts = iterator->second;
                if (counts.triangles == 6 && counts.squares == 0) {
                    candidates_.erase(vertex);
                }
                if (tile.sides == 3) {
                    counts.triangles += change;
                } else {
                    counts.squares += change;
                }
                if (central) {
                    counts.central += change;
                }
                if (counts.triangles == 6 && counts.squares == 0) {
                    candidates_.insert(vertex);
                }
                if (
                    counts.triangles == 0
                    && counts.squares == 0
                    && counts.central == 0
                ) {
                    incidence_.erase(iterator);
                }
            }
        }
    }

    std::uint32_t parent_of(std::uint32_t word) const {
        for (int index = 0; index < 2 * side_length_ - 1; ++index) {
            const bool first = word & (1U << index);
            const bool second = word & (1U << (index + 1));
            if (!first && second) {
                return word ^ (3U << index);
            }
        }
        return word;
    }

    void visit(std::uint32_t word) {
        ++visited_;
        without_dodecagon_ += all_independent_sets(candidates_);
        without_dodecagon_ %= MODULUS;

        const bool first_bit = word & 1U;
        const bool second_bit = word & 2U;
        if (first_bit != second_bit) {
            std::unordered_set<Point, PointHash> allowed;
            allowed.reserve(candidates_.size());
            for (const Point& point : candidates_) {
                if (incidence_.at(point).central == 0) {
                    allowed.insert(point);
                }
            }
            refined_dodecagon_ += all_independent_sets(allowed);
            refined_dodecagon_ %= MODULUS;
        }

        for (int index = 0; index < 2 * side_length_ - 1; ++index) {
            const bool first_bit_here = word & (1U << index);
            const bool second_bit_here = word & (1U << (index + 1));
            if (!first_bit_here || second_bit_here) {
                continue;
            }
            const std::uint32_t child = word ^ (3U << index);
            if (parent_of(child) != word) {
                continue;
            }

            const std::uint32_t prefix_mask = (
                index == 0 ? 0U : (1U << index) - 1
            );
            const int first_count = __builtin_popcount(word & prefix_mask);
            const int second_count = index - first_count;

            update_tiles(corona(first_count, second_count, true), -1);
            update_tiles(corona(first_count + 1, second_count, false), -1);
            update_tiles(corona(first_count, second_count, false), 1);
            update_tiles(corona(first_count, second_count + 1, true), 1);

            visit(child);

            update_tiles(corona(first_count, second_count + 1, true), -1);
            update_tiles(corona(first_count, second_count, false), -1);
            update_tiles(corona(first_count + 1, second_count, false), 1);
            update_tiles(corona(first_count, second_count, true), 1);
        }
    }
};

i64 count_tilings(int side_length) {
    Counter counter(side_length);
    return counter.run();
}

}  // namespace

int main(int argc, char** argv) {
    const int side_length = argc > 1 ? std::stoi(argv[1]) : 10;
    assert(1 <= side_length && side_length <= 10);
    const i64 result = count_tilings(side_length);
    if (side_length == 1) {
        assert(result == 5);
    }
    if (side_length == 2) {
        assert(result == 48);
    }
    std::cout << result << '\n';
}
