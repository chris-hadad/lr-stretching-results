// Fresh finite rank-six hive certificate verifier. C++17, standard library only.
// Usage: topology_core DATA_DIRECTORY MODE PREFIX_COUNT MUTATION
// Modes: q5, q6, types6, matrix5, matrix6. MUTATION is normally "none".
// No returned implementation is linked, imported, or executed.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <sys/resource.h>
#include <unordered_map>
#include <vector>

using Bytes = std::vector<unsigned char>;
using Row = std::array<int, 10>;
using Point = std::array<int, 2>;
using Clock = std::chrono::steady_clock;
static auto started = Clock::now();
static std::string directory, mutation;

void require(bool ok, const std::string& reason) {
    if (!ok) throw std::runtime_error(reason);
}
double elapsed() { return std::chrono::duration<double>(Clock::now() - started).count(); }
void deadline() {
    require(elapsed() < 110.0, "INTERNAL_110_SECOND_DEADLINE");
    struct rusage usage{}; getrusage(RUSAGE_SELF, &usage);
#ifdef __APPLE__
    uint64_t bytes = usage.ru_maxrss;
#else
    uint64_t bytes = uint64_t(usage.ru_maxrss) * 1024;
#endif
    require(bytes < 900ULL * 1024 * 1024, "HELPER_RSS_LIMIT");
}
Bytes file(const std::string& name, size_t expected) {
    std::ifstream in(directory + "/" + name, std::ios::binary | std::ios::ate);
    require(bool(in), "MISSING_INPUT_" + name);
    require(size_t(in.tellg()) == expected, "WRONG_INPUT_SIZE_" + name);
    Bytes out(expected);
    in.seekg(0);
    in.read(reinterpret_cast<char*>(out.data()), out.size());
    require(bool(in) || out.empty(), "INCOMPLETE_INPUT_" + name);
    return out;
}
uint64_t unsigned_at(const Bytes& b, size_t pos, size_t width) {
    require(pos <= b.size() && width <= b.size() - pos, "TRUNCATED_TYPED_RECORD");
    uint64_t value = 0;
    for (size_t j = 0; j < width; ++j) value |= uint64_t(b[pos + j]) << (8 * j);
    return value;
}
int64_t signed_at(const Bytes& b, size_t pos, size_t width) {
    auto u = unsigned_at(b, pos, width);
    uint64_t sign = uint64_t(1) << (8 * width - 1);
    return (u & sign) ? -int64_t((uint64_t(1) << (8 * width)) - u) : int64_t(u);
}
int64_t checked(__int128 value) {
    require(value > -(__int128(1) << 60) && value < (__int128(1) << 60), "INTEGER_RANGE_REFUSAL");
    return int64_t(value);
}
uint64_t mask(const std::vector<int>& ids) {
    uint64_t out = 0;
    int before = -1;
    for (int id : ids) {
        require(before < id && id < 42, "NORMAL_SUBSET_ORDER_OR_RANGE");
        out |= uint64_t(1) << id;
        before = id;
    }
    return out;
}
uint64_t choose(int n, int k) {
    if (k < 0 || n < k) return 0;
    uint64_t x = 1;
    for (int j = 1; j <= k; ++j) x = x * (n - j + 1) / j;
    return x;
}
uint64_t ordinal(const std::vector<int>& ids) {
    uint64_t total = 0;
    int previous = -1;
    for (size_t j = 0; j < ids.size(); ++j) {
        for (int v = previous + 1; v < ids[j]; ++v)
            total += choose(41 - v, int(ids.size() - j - 1));
        previous = ids[j];
    }
    return total;
}
template<class F> void subsets(int k, uint64_t limit, F visit) {
    require(limit > 0 && limit <= choose(42, k), "SUBSET_PREFIX_RANGE");
    std::vector<int> ids(k);
    std::iota(ids.begin(), ids.end(), 0);
    for (uint64_t i = 0; i < limit; ++i) {
        visit(ids, i);
        if (i % 1000 == 0) deadline();
        if (i + 1 == limit) break;
        int p = k - 1;
        while (p >= 0 && ids[p] == 42 - k + p) --p;
        require(p >= 0, "PREMATURE_SUBSET_END");
        ++ids[p];
        for (int j = p + 1; j < k; ++j) ids[j] = ids[j - 1] + 1;
    }
}

struct Geometry {
    std::vector<Row> normals;
    std::vector<std::array<int, 42>> actions;
    Geometry() {
        std::vector<Point> vertices, interior;
        for (int i = 0; i <= 6; ++i) for (int j = 0; i + j <= 6; ++j) vertices.push_back({i, j});
        for (auto p : vertices) if (p[0] > 0 && p[1] > 0 && p[0] + p[1] < 6) interior.push_back(p);
        require(vertices.size() == 28 && interior.size() == 10, "HIVE_VERTEX_DIMENSIONS");
        std::map<Point, int> vertex_id, interior_id;
        for (size_t i = 0; i < vertices.size(); ++i) vertex_id[vertices[i]] = i;
        for (size_t i = 0; i < interior.size(); ++i) interior_id[interior[i]] = i;
        // Each pair meets at 60 degrees in the equilateral triangular lattice.
        // The two obtuse vertices have +1 coefficients in the inward inequality.
        std::array<std::array<Point, 2>, 3> directions = {{{{{1, 0}, {0, 1}}}, {{{1, 0}, {1, -1}}}, {{{0, 1}, {-1, 1}}}}};
        std::set<std::array<int, 28>> rhombi;
        std::set<Row> normal_set;
        for (auto p : vertices) for (auto pair : directions) {
            auto a = pair[0], b = pair[1];
            std::array<Point, 4> corners = {p, Point{p[0] + a[0], p[1] + a[1]},
                Point{p[0] + b[0], p[1] + b[1]}, Point{p[0] + a[0] + b[0], p[1] + a[1] + b[1]}};
            bool inside = true;
            for (auto x : corners) inside &= vertex_id.count(x) != 0;
            if (!inside) continue;
            std::array<int, 28> full{};
            Row reduced{};
            const int signs[] = {-1, 1, 1, -1};
            for (int j = 0; j < 4; ++j) {
                full[vertex_id.at(corners[j])] = signs[j];
                auto at = interior_id.find(corners[j]);
                if (at != interior_id.end()) reduced[at->second] = signs[j];
            }
            require(rhombi.insert(full).second, "DUPLICATE_GEOMETRIC_RHOMBUS");
            int divisor = 0;
            for (int x : reduced) divisor = std::gcd(divisor, std::abs(x));
            require(divisor == 1, "NONPRIMITIVE_OR_ZERO_HIVE_NORMAL");
            normal_set.insert(reduced);
        }
        require(rhombi.size() == 45 && normal_set.size() == 42, "RHOMBUS_OR_NORMAL_UNIVERSE_COUNT");
        normals.assign(normal_set.begin(), normal_set.end());
        std::map<Row, int> normal_id;
        for (int i = 0; i < 42; ++i) normal_id[normals[i]] = i;
        std::array<int, 3> permutation{0, 1, 2};
        do {
            auto transform = [&](Point p) {
                int bary[] = {p[0], p[1], 6 - p[0] - p[1]};
                return Point{bary[permutation[0]], bary[permutation[1]]};
            };
            for (auto full : rhombi) {
                std::array<int, 28> transported{};
                for (int i = 0; i < 28; ++i) transported[vertex_id.at(transform(vertices[i]))] = full[i];
                require(rhombi.count(transported), "ACTION_DOES_NOT_PRESERVE_ORIENTED_RHOMBI");
            }
            std::array<int, 10> coord{};
            std::set<int> coord_seen;
            for (int i = 0; i < 10; ++i) { coord[i] = interior_id.at(transform(interior[i])); coord_seen.insert(coord[i]); }
            require(coord_seen.size() == 10, "ACTION_NOT_INTEGER_ORTHOGONAL_PERMUTATION");
            std::array<int, 42> action{};
            for (int i = 0; i < 42; ++i) {
                Row transported{};
                for (int j = 0; j < 10; ++j) transported[coord[j]] = normals[i][j];
                require(normal_id.count(transported), "ACTION_NORMAL_NOT_IN_ATLAS");
                action[i] = normal_id.at(transported);
            }
            actions.push_back(action);
        } while (std::next_permutation(permutation.begin(), permutation.end()));
        std::ifstream input(directory + "/atlas.txt");
        int dim, count, order;
        input >> dim >> count >> order;
        require(bool(input) && dim == 10 && count == 42 && order == 6, "SOURCE_ATLAS_HEADER");
        for (int i = 0; i < 42; ++i) for (int j = 0; j < 10; ++j) {
            int x; input >> x;
            if (mutation == "normal" && i == 0 && j == 0) ++x;
            require(bool(input) && x == normals[i][j], "FRESH_NORMAL_ATLAS_DISAGREEMENT");
        }
        std::set<std::array<int, 42>> supplied, fresh(actions.begin(), actions.end());
        for (int i = 0; i < 6; ++i) {
            std::array<int, 42> action{};
            for (int& x : action) input >> x;
            require(bool(input), "INCOMPLETE_SOURCE_ACTION");
            supplied.insert(action);
        }
        std::string extra;
        require(!(input >> extra) && supplied == fresh && fresh.size() == 6, "FRESH_SIX_ACTIONS_DISAGREE");
    }
    std::vector<int> image(const std::vector<int>& ids, size_t action) const {
        std::vector<int> result;
        for (int id : ids) result.push_back(actions[action][id]);
        std::sort(result.begin(), result.end());
        return result;
    }
    std::vector<int> anchor(const std::vector<int>& ids) const {
        auto result = ids;
        for (size_t g = 0; g < 6; ++g) result = std::min(result, image(ids, g));
        return result;
    }
};

// Unimodular integer column operations reduce the row lattice to a triangular
// full-rank block. The product of pivots is the gcd of all maximal minors.
int lattice_index(const Geometry& g, const std::vector<int>& ids) {
    size_t k = ids.size();
    int64_t matrix[6][10]{};
    for (size_t i = 0; i < k; ++i) for (int j = 0; j < 10; ++j) matrix[i][j] = g.normals[ids[i]][j];
    int64_t determinant = 1;
    for (size_t r = 0; r < k; ++r) {
        size_t pivot = r;
        while (pivot < 10 && matrix[r][pivot] == 0) ++pivot;
        if (pivot == 10) return 0;
        for (size_t i = 0; i < k; ++i) std::swap(matrix[i][r], matrix[i][pivot]);
        for (size_t col = r + 1; col < 10; ++col) {
            while (matrix[r][col] != 0) {
                int64_t quotient = matrix[r][r] / matrix[r][col];
                for (size_t i = 0; i < k; ++i) matrix[i][r] = checked(__int128(matrix[i][r]) - __int128(quotient) * matrix[i][col]);
                for (size_t i = 0; i < k; ++i) std::swap(matrix[i][r], matrix[i][col]);
            }
        }
        determinant = checked(__int128(determinant) * matrix[r][r]);
    }
    require(std::abs(determinant) <= 65535, "NORMAL_INDEX_OUTSIDE_RECORD_RANGE");
    return int(std::abs(determinant));
}

struct Kernel {
    std::vector<int> ids;
    int index;
    int64_t m[10][6]{}, left[6][10]{};
};
std::vector<Kernel> kernels(const Geometry& g, int q) {
    int support = q - 1, dimension = 11 - q;
    size_t count = q == 5 ? 17165 : 121241;
    size_t record = q == 5 ? 486 : 207;
    size_t width = q == 5 ? 4 : 2;
    Bytes raw = file(q == 5 ? "q5-kernels.bin" : "q6-kernels.bin", count * record);
    std::vector<Kernel> result(count);
    for (size_t row = 0; row < count; ++row) {
        auto& k = result[row];
        size_t offset = row * record;
        for (int i = 0; i < support; ++i) k.ids.push_back(raw[offset++]);
        mask(k.ids);
        k.index = unsigned_at(raw, offset, 2); offset += 2;
        require(k.index > 0 && k.index == lattice_index(g, k.ids), "FRESH_KERNEL_SUPPORT_INDEX");
        for (int i = 0; i < 10; ++i) for (int j = 0; j < dimension; ++j) { k.m[i][j] = signed_at(raw, offset, width); offset += width; }
        for (int i = 0; i < dimension; ++i) for (int j = 0; j < 10; ++j) { k.left[i][j] = signed_at(raw, offset, width); offset += width; }
        if (mutation == "kernel" && row == 0) ++k.m[0][0];
        for (int i = 0; i < support; ++i) for (int j = 0; j < dimension; ++j) {
            __int128 value = 0;
            for (int c = 0; c < 10; ++c) value += __int128(g.normals[k.ids[i]][c]) * k.m[c][j];
            require(checked(value) == 0, "KERNEL_NOT_ANNIHILATED_BY_SUPPORT");
        }
        for (int i = 0; i < dimension; ++i) for (int j = 0; j < dimension; ++j) {
            __int128 value = 0;
            for (int c = 0; c < 10; ++c) value += __int128(k.left[i][c]) * k.m[c][j];
            require(checked(value) == (i == j), "KERNEL_INTEGER_LEFT_INVERSE_FAILS");
        }
        require(row == 0 || result[row - 1].ids < k.ids, "KERNEL_SUPPORT_ORDER_OR_DUPLICATE");
        require(g.anchor(k.ids) == k.ids, "KERNEL_SUPPORT_NOT_CANONICAL_ORBIT");
        if (row % 1000 == 0) deadline();
    }
    return result;
}
struct Orbit {
    std::vector<int> ids;
    int index;
    uint32_t type = 0, count = 0, original;
};
std::vector<Orbit> orbits(int q) {
    size_t count = q == 5 ? 121241 : 675721, record = q == 5 ? 19 : 12;
    auto raw = file(q == 5 ? "q5-orbits.bin" : "q6-orbits.bin", count * record);
    std::vector<Orbit> result(count);
    for (size_t r = 0; r < count; ++r) {
        auto& o = result[r];
        size_t pos = r * record;
        for (int i = 0; i < q; ++i) o.ids.push_back(raw[pos++]);
        mask(o.ids);
        o.index = unsigned_at(raw, pos, 2); pos += 2;
        if (q == 5) { o.type = unsigned_at(raw, pos, 4); pos += 4; o.count = unsigned_at(raw, pos, 4); pos += 4; }
        o.original = unsigned_at(raw, pos, 4);
        if (mutation == "orbit" && r == 0) ++o.original;
        require(o.index > 0 && ordinal(o.ids) == o.original, "ORBIT_ORIGINAL_ORDINAL_IDENTITY");
        require(r == 0 || result[r - 1].ids < o.ids, "ORBIT_ORDER_OR_DUPLICATE");
    }
    return result;
}

struct Type5 {
    int index, kind, key[50]{}, perm[5]{}, gram[5][5]{};
    std::vector<int> ids;
    uint32_t count;
};
std::array<int, 50> column_key5(const Geometry& g, const std::vector<int>& ids, const int* perm) {
    std::array<std::array<int, 5>, 10> columns{};
    for (int c = 0; c < 10; ++c) {
        int sign = 1;
        for (int j = 0; j < 5; ++j) if (g.normals[ids[perm[j]]][c]) { sign = g.normals[ids[perm[j]]][c] < 0 ? -1 : 1; break; }
        for (int j = 0; j < 5; ++j) columns[c][j] = sign * g.normals[ids[perm[j]]][c];
    }
    std::sort(columns.begin(), columns.end());
    std::array<int, 50> out{};
    for (int c = 0; c < 10; ++c) for (int j = 0; j < 5; ++j) out[c * 5 + j] = columns[c][j];
    return out;
}
bool explicit_key5(const Geometry& g, const std::vector<int>& ids, const Type5& type, const int* p) {
    if (type.kind == 1) {
        for (int i = 0; i < 5; ++i) for (int j = 0; j < 5; ++j) {
            int z = std::inner_product(g.normals[ids[p[i]]].begin(), g.normals[ids[p[i]]].end(), g.normals[ids[p[j]]].begin(), 0);
            if (z != type.key[5 * i + j]) return false;
        }
        return true;
    }
    auto key = column_key5(g, ids, p);
    return std::equal(key.begin(), key.end(), type.key);
}
std::vector<Type5> types5(const Geometry& g) {
    auto raw = file("q5-types.bin", 39974 * 67);
    std::vector<Type5> out(39974);
    std::set<std::vector<int>> distinct;
    for (int t = 0; t < 39974; ++t) {
        auto& x = out[t];
        size_t pos = 67 * t;
        x.index = unsigned_at(raw, pos, 2); pos += 2;
        for (int i = 0; i < 5; ++i) x.ids.push_back(raw[pos++]);
        mask(x.ids);
        x.kind = raw[pos++];
        for (int& k : x.key) k = signed_at(raw, pos++, 1);
        for (int& p : x.perm) p = raw[pos++];
        if (mutation == "type-permutation" && t == 0) x.perm[0] = x.perm[1];
        auto sorted = std::vector<int>(x.perm, x.perm + 5);
        std::sort(sorted.begin(), sorted.end());
        require(sorted == std::vector<int>({0, 1, 2, 3, 4}), "INVALID_Q5_GENERATOR_PERMUTATION");
        x.count = unsigned_at(raw, pos, 4);
        require(x.count > 0 && x.index == lattice_index(g, x.ids), "Q5_TYPE_REPRESENTATIVE_INDEX");
        require((x.index == 1 && x.kind == 1) || (x.index > 1 && x.kind == 2), "UNSAFE_Q5_TYPE_KEY_KIND");
        if (x.kind == 1) for (int i = 25; i < 50; ++i) require(x.key[i] == 0, "Q5_GRAM_KEY_NONZERO_PADDING");
        require(explicit_key5(g, x.ids, x, x.perm), "Q5_TYPE_REPRESENTATIVE_SAFE_KEY");
        std::vector<int> key{x.index, x.kind}; key.insert(key.end(), x.key, x.key + 50);
        require(distinct.insert(key).second, "DUPLICATE_Q5_SAFE_TYPE_KEY");
        for (int i = 0; i < 5; ++i) for (int j = 0; j < 5; ++j) {
            if (x.kind == 1) x.gram[i][j] = x.key[5 * i + j];
            else for (int c = 0; c < 10; ++c) x.gram[i][j] += x.key[5 * c + i] * x.key[5 * c + j];
        }
        if (t % 1000 == 0) deadline();
    }
    return out;
}
bool safe_reuse5(const Geometry& g, const std::vector<int>& ids, const Type5& type) {
    int gram[5][5]{};
    for (int i = 0; i < 5; ++i) for (int j = 0; j < 5; ++j)
        gram[i][j] = std::inner_product(g.normals[ids[i]].begin(), g.normals[ids[i]].end(), g.normals[ids[j]].begin(), 0);
    int p[5]{};
    std::function<bool(int, int)> search = [&](int at, int used) {
        if (at == 5) return explicit_key5(g, ids, type, p);
        for (int candidate = 0; candidate < 5; ++candidate) {
            if (used & (1 << candidate)) continue;
            bool consistent = gram[candidate][candidate] == type.gram[at][at];
            for (int j = 0; j < at; ++j) consistent &= gram[candidate][p[j]] == type.gram[at][j];
            if (consistent) { p[at] = candidate; if (search(at + 1, used | (1 << candidate))) return true; }
        }
        return false;
    };
    return search(0, 0);
}

using Metrics = std::map<std::string, uint64_t>;
Metrics verify5(const Geometry& g, uint64_t stop) {
    auto types = types5(g);
    auto rows = orbits(5);
    auto matrix_types = file("q5-type_ids.bin", 121241 * 4);
    for (size_t i = 0; i < rows.size(); ++i)
        require(rows[i].type == unsigned_at(matrix_types, 4 * i, 4), "Q5_LITERAL_MATRIX_TYPE_MAP_JOIN");
    auto support = kernels(g, 5);
    auto raw = file("q5-tuples.bin", 850668 * 11);
    auto map = file("q5-tuple-orbit.bin", 850668 * 4);
    std::unordered_map<uint64_t, size_t> row_id, support_id;
    for (size_t i = 0; i < rows.size(); ++i) require(row_id.emplace(mask(rows[i].ids), i).second, "DUPLICATE_Q5_ORBIT");
    for (size_t i = 0; i < support.size(); ++i) support_id[mask(support[i].ids)] = i;
    std::vector<uint32_t> type_counts(types.size()), orbit_counts(rows.size()), support_counts(support.size());
    uint64_t independent4 = 0;
    subsets(4, choose(42, 4), [&](const auto& ids, auto) {
        int ix = lattice_index(g, ids);
        if (!ix) return;
        ++independent4;
        auto canonical = g.anchor(ids);
        auto at = support_id.find(mask(canonical));
        require(at != support_id.end() && support[at->second].index == ix, "COMPLETE_FOUR_SUPPORT_ORBIT_COVER");
        ++support_counts[at->second];
    });
    require(independent4 == 102297 && std::all_of(support_counts.begin(), support_counts.end(), [](auto n){return n > 0;}), "FOUR_SUPPORT_COMPLETE_POPULATION");
    Metrics stats{{"four_subsets_checked", choose(42, 4)}, {"independent_four_supports", independent4}, {"four_support_orbits", support.size()}, {"q5_type_representatives", types.size()}, {"matrix_type_map_rows", rows.size()}};
    subsets(5, stop, [&](const auto& ids, uint64_t position) {
        size_t at = position * 11;
        for (int j = 0; j < 5; ++j) require(raw[at + j] == ids[j], "Q5_LITERAL_TUPLE_ORDER");
        int stored = unsigned_at(raw, at + 5, 2);
        if (mutation == "index" && position == 0) ++stored;
        int fresh = lattice_index(g, ids);
        require(fresh == stored, "Q5_FRESH_NORMAL_INDEX_DISAGREEMENT");
        uint32_t tid = unsigned_at(raw, at + 7, 4), oid = unsigned_at(map, position * 4, 4);
        if (!fresh) { require(tid == UINT32_MAX && oid == UINT32_MAX, "Q5_DEPENDENT_SENTINEL"); ++stats["dependent"]; return; }
        ++stats["independent"];
        require(tid < types.size() && types[tid].index == fresh && safe_reuse5(g, ids, types[tid]), "Q5_COMPLETE_SAFE_TYPE_WITNESS");
        ++type_counts[tid];
        auto canonical = g.anchor(ids);
        auto found = row_id.find(mask(canonical));
        require(found != row_id.end() && found->second == oid, "Q5_COMPLETE_TUPLE_TO_ORBIT_MAP");
        auto& row = rows[oid];
        require(row.index == fresh && row.type == tid, "Q5_ORBIT_INDEX_TYPE_JOIN");
        ++orbit_counts[oid];
        ++stats["index_" + std::to_string(fresh)];
    });
    stats["tuples_checked"] = stop;
    if (stop == 850668) {
        require(stats["independent"] == 725697 && stats["dependent"] == 124971, "Q5_COMPLETE_INDEPENDENT_COMPLEMENT");
        for (size_t i = 0; i < types.size(); ++i) require(types[i].count == type_counts[i], "Q5_COMPLETE_TYPE_OCCURRENCE_COUNTS");
        for (size_t i = 0; i < rows.size(); ++i) require(rows[i].count == orbit_counts[i] && orbit_counts[i] > 0, "Q5_COMPLETE_ORBIT_OCCURRENCE_COUNTS");
        stats["complete"] = 1;
    }
    return stats;
}

Metrics verify6(const Geometry& g, uint64_t stop) {
    auto supports = kernels(g, 6);
    auto inherited_rows = orbits(5);
    require(inherited_rows.size() == supports.size(), "Q6_Q5_SUPPORT_ROSTER_LENGTH");
    for (size_t i = 0; i < supports.size(); ++i)
        require(supports[i].ids == inherited_rows[i].ids && supports[i].index == inherited_rows[i].index,
                "Q6_KERNEL_LITERAL_Q5_SUPPORT_ORBIT_JOIN");
    auto rows = orbits(6);
    auto q5 = file("q5-tuples.bin", 850668 * 11);
    auto q6 = file("q6-indices-full.bin", 5245786 * 2);
    std::unordered_map<uint64_t, size_t> support_id;
    for (size_t i = 0; i < supports.size(); ++i) support_id[mask(supports[i].ids)] = i;
    // Each inherited prefix index is recomputed when the prefix changes. Thus
    // this pass does not merely trust a prior q5 pass to classify q6 dependency.
    std::vector<int> previous;
    int prefix_index = 0, action = -1;
    const Kernel* kernel = nullptr;
    uint64_t next_orbit = 0;
    Metrics stats{{"five_support_kernels", supports.size()}};
    subsets(6, stop, [&](const auto& ids, uint64_t pos) {
        std::vector<int> prefix(ids.begin(), ids.begin() + 5);
        if (prefix != previous) {
            previous = prefix;
            prefix_index = lattice_index(g, prefix);
            auto ord = ordinal(prefix);
            for (int j = 0; j < 5; ++j) require(q5[11 * ord + j] == prefix[j], "Q6_PREFIX_Q5_LITERAL_JOIN");
            require(unsigned_at(q5, 11 * ord + 5, 2) == uint64_t(prefix_index), "Q6_FRESH_PREFIX_INDEX_JOIN");
            if (prefix_index) {
                auto anchor = g.anchor(prefix);
                auto found = support_id.find(mask(anchor));
                require(found != support_id.end(), "Q6_COMPLETE_FIVE_SUPPORT_COVER");
                kernel = &supports[found->second];
                require(kernel->index == prefix_index, "Q6_PREFIX_SUPPORT_INDEX");
                action = -1;
                for (int a = 0; a < 6; ++a) if (g.image(prefix, a) == anchor) { action = a; break; }
                require(action >= 0, "Q6_PREFIX_TRANSPORT_MISSING");
            }
        }
        int fresh = 0;
        if (prefix_index) {
            int normal = g.actions[action][ids[5]];
            int64_t divisor = 0;
            for (int c = 0; c < 5; ++c) {
                __int128 restricted = 0;
                for (int j = 0; j < 10; ++j) restricted += __int128(kernel->m[j][c]) * g.normals[normal][j];
                divisor = std::gcd(divisor, std::abs(checked(restricted)));
            }
            fresh = int(checked(__int128(prefix_index) * divisor));
        }
        int stored = unsigned_at(q6, 2 * pos, 2);
        if (mutation == "index" && pos == 0) ++stored;
        require(fresh == stored, "Q6_COMPLETE_FRESH_QUOTIENT_INDEX_DISAGREEMENT");
        ++stats["index_" + std::to_string(fresh)];
        if (!fresh) { ++stats["dependent"]; return; }
        ++stats["independent"];
        auto canonical = g.anchor(ids);
        if (canonical == ids) {
            require(next_orbit < rows.size(), "EXTRA_Q6_CANONICAL_ORBIT");
            auto& row = rows[next_orbit++];
            require(row.ids == ids && row.index == fresh && row.original == pos, "Q6_COMPLETE_CANONICAL_ORBIT_IDENTITY");
        }
    });
    stats["tuples_checked"] = stop;
    stats["canonical_orbits_checked"] = next_orbit;
    if (stop == 5245786) {
        require(next_orbit == 675721 && stats["independent"] == 4050197 && stats["dependent"] == 1195589, "Q6_FULL_ORBIT_AND_COMPLEMENT_COUNTS");
        stats["complete"] = 1;
    }
    return stats;
}

std::array<unsigned char, 61> key6(const Geometry& g, const Orbit& row, const unsigned char* p) {
    std::set<int> used(p, p + 6);
    require(used == std::set<int>({0, 1, 2, 3, 4, 5}), "INVALID_Q6_GENERATOR_PERMUTATION");
    std::array<unsigned char, 61> result{};
    result[0] = row.index;
    int at = 1;
    if (row.index == 1) {
        for (int i = 0; i < 6; ++i) for (int j = i; j < 6; ++j) {
            int x = std::inner_product(g.normals[row.ids[p[i]]].begin(), g.normals[row.ids[p[i]]].end(), g.normals[row.ids[p[j]]].begin(), 0);
            require(x + 4 >= 0 && x + 4 <= 255, "Q6_GRAM_KEY_ENCODING_RANGE");
            result[at++] = x + 4;
        }
    } else {
        std::array<std::array<int, 6>, 10> columns{};
        for (int c = 0; c < 10; ++c) {
            int sign = 1;
            for (int i = 0; i < 6; ++i) if (g.normals[row.ids[p[i]]][c]) { sign = g.normals[row.ids[p[i]]][c] < 0 ? -1 : 1; break; }
            for (int i = 0; i < 6; ++i) columns[c][i] = sign * g.normals[row.ids[p[i]]][c];
        }
        std::sort(columns.begin(), columns.end());
        for (auto col : columns) for (int x : col) { require(x >= -1 && x <= 1, "Q6_EMBEDDING_KEY_ENCODING"); result[at++] = x + 1; }
    }
    return result;
}
Metrics verify_types6(const Geometry& g, uint64_t stop) {
    require(stop > 0 && stop <= 675721, "Q6_TYPE_PREFIX_RANGE");
    auto rows = orbits(6);
    auto keys = file("q6-keys.bin", 675721 * 67);
    auto types = file("q6-TYPES.bin", 293795 * 71);
    auto counts = file("q6-TYPE-COUNTS.bin", 293795 * 4);
    auto mapping = file("q6-ORBIT-TYPE.bin", 675721 * 4);
    std::set<std::array<unsigned char, 61>> distinct;
    for (uint64_t t = 0; t < 293795; ++t) {
        uint64_t first = unsigned_at(types, 71 * t + 61, 4);
        require(first < 675721 && unsigned_at(mapping, 4 * first, 4) == t, "Q6_TYPE_REPRESENTATIVE_ROW_JOIN");
        require(lattice_index(g, rows[first].ids) == rows[first].index, "Q6_TYPE_REPRESENTATIVE_FRESH_INDEX");
        auto computed = key6(g, rows[first], types.data() + 71 * t + 65);
        require(std::equal(computed.begin(), computed.end(), types.begin() + 71 * t), "Q6_TYPE_REPRESENTATIVE_KEY_WITNESS");
        require(distinct.insert(computed).second, "Q6_DUPLICATE_SAFE_KEY");
        if (t % 1000 == 0) deadline();
    }
    std::vector<uint32_t> observed(293795);
    Metrics stats{{"type_representatives_checked", 293795}};
    for (uint64_t r = 0; r < stop; ++r) {
        require(lattice_index(g, rows[r].ids) == rows[r].index, "Q6_ORBIT_WITNESS_FRESH_INDEX");
        unsigned char permutation[6]; std::copy_n(keys.begin() + 67 * r + 61, 6, permutation);
        if (mutation == "type-permutation" && r == 0) permutation[0] = permutation[1];
        auto computed = key6(g, rows[r], permutation);
        require(std::equal(computed.begin(), computed.end(), keys.begin() + 67 * r), "Q6_EVERY_ORBIT_SAFE_KEY_WITNESS");
        uint32_t tid = unsigned_at(mapping, 4 * r, 4);
        require(tid < 293795 && std::equal(computed.begin(), computed.end(), types.begin() + 71 * tid), "Q6_EVERY_ORBIT_TO_TYPE_IDENTITY");
        ++observed[tid];
        ++stats[rows[r].index == 1 ? "index_one_orbits" : "higher_index_orbits"];
        if (r % 1000 == 0) deadline();
    }
    stats["orbit_witnesses_checked"] = stop;
    if (stop == 675721) {
        for (uint64_t t = 0; t < 293795; ++t) require(observed[t] > 0 && observed[t] == unsigned_at(counts, 4 * t, 4), "Q6_COMPLETE_TYPE_OCCURRENCE_COUNTS");
        stats["complete"] = 1;
    }
    return stats;
}

Metrics verify_matrix(const Geometry& g, int q, uint64_t stop) {
    size_t total = q == 5 ? 121241 : 675721, nz = q == 5 ? 1307258 : 8139966;
    int dimension = 11 - q;
    require(stop > 0 && stop <= total, "MATRIX_PREFIX_RANGE");
    auto support = kernels(g, q);
    auto rows = orbits(q);
    auto ptr = file("q" + std::to_string(q) + "-indptr.bin", (total + 1) * 4);
    auto cols = file("q" + std::to_string(q) + "-indices.bin", nz * 4);
    auto data = file("q" + std::to_string(q) + "-data.bin", nz * 4);
    require(unsigned_at(ptr, 0, 4) == 0 && unsigned_at(ptr, total * 4, 4) == nz, "MATRIX_CSR_FULL_ENDPOINTS");
    std::unordered_map<uint64_t, size_t> support_id;
    for (size_t i = 0; i < support.size(); ++i) support_id[mask(support[i].ids)] = i;
    Metrics stats{{"saturated_kernels_checked", support.size()}};
    for (uint64_t row = 0; row < stop; ++row) {
        const auto& cone = rows[row];
        require(lattice_index(g, cone.ids) == cone.index, "MATRIX_ROW_FRESH_NORMAL_INDEX");
        std::map<int, int64_t> expected;
        for (int omit = 0; omit < q; ++omit) {
            std::vector<int> face;
            for (int j = 0; j < q; ++j) if (j != omit) face.push_back(cone.ids[j]);
            auto anchor = g.anchor(face);
            auto found = support_id.find(mask(anchor));
            require(found != support_id.end(), "MATRIX_COMPLETE_SUPPORT_INCIDENCE");
            auto& kernel = support[found->second];
            std::array<int64_t, 6> primitive_sum{};
            int transports = 0;
            for (int a = 0; a < 6; ++a) {
                if (g.image(face, a) != anchor) continue;
                ++transports;
                int normal = g.actions[a][cone.ids[omit]];
                std::array<int64_t, 6> vector{};
                int64_t divisor = 0;
                for (int c = 0; c < dimension; ++c) {
                    __int128 sum = 0;
                    for (int j = 0; j < 10; ++j) sum += __int128(kernel.m[j][c]) * g.normals[normal][j];
                    vector[c] = checked(sum);
                    divisor = std::gcd(divisor, std::abs(vector[c]));
                }
                if (mutation == "primitive-divisor" && row == 0 && omit == 0) ++divisor;
                require(divisor > 0 && checked(__int128(divisor) * kernel.index) == cone.index, "PRIMITIVE_QUOTIENT_DIVISOR_IDENTITY");
                for (int c = 0; c < dimension; ++c) {
                    require(vector[c] % divisor == 0, "NONINTEGRAL_PRIMITIVE_QUOTIENT");
                    primitive_sum[c] = checked(__int128(primitive_sum[c]) + vector[c] / divisor);
                }
                ++stats["primitive_divisor_" + std::to_string(divisor)];
            }
            require(transports > 0 && 6 % transports == 0, "INCOMPLETE_STABILIZER_COSET");
            ++stats["stabilizer_" + std::to_string(transports)];
            ++stats["incidences_checked"];
            for (int c = 0; c < dimension; ++c) {
                __int128 numerator = __int128(6) * primitive_sum[c];
                require(numerator % transports == 0, "NONINTEGRAL_SIXFOLD_AVERAGE");
                int col = dimension * found->second + c;
                expected[col] = checked(__int128(expected[col]) + numerator / transports);
            }
        }
        for (auto at = expected.begin(); at != expected.end();) {
            if (at->second == 0) at = expected.erase(at); else ++at;
        }
        uint64_t lo = unsigned_at(ptr, 4 * row, 4), hi = unsigned_at(ptr, 4 * (row + 1), 4);
        require(lo <= hi && hi <= nz, "CSR_POINTER_ORDER");
        std::map<int, int64_t> actual;
        int previous = -1;
        for (uint64_t at = lo; at < hi; ++at) {
            int col = unsigned_at(cols, 4 * at, 4);
            int64_t value = signed_at(data, 4 * at, 4);
            require(previous < col && col < dimension * int(support.size()) && value != 0, "CSR_CANONICAL_COMPLETE_ROW");
            if (mutation == "matrix-entry" && row == 0 && at == lo) ++value;
            actual[col] = value;
            previous = col;
        }
        if (mutation == "omitted-matrix-entry" && row == 0 && !actual.empty()) actual.erase(actual.begin());
        require(expected == actual, "COMPLETE_MATRIX_ROW_OR_OMITTED_ZERO_MISMATCH");
        stats["entries_checked"] += hi - lo;
        if (row % 1000 == 0) deadline();
    }
    stats["rows_checked"] = stop;
    stats["columns"] = dimension * support.size();
    stats["integer_scale"] = 6;
    if (stop == total) { require(stats["entries_checked"] == nz, "MATRIX_INCOMPLETE_FULL_ENTRY_COVERAGE"); stats["complete"] = 1; }
    return stats;
}

int main(int argc, char** argv) {
    try {
        require(argc == 5, "USAGE_DATA_DIRECTORY_MODE_PREFIX_COUNT_MUTATION");
        directory = argv[1];
        std::string mode = argv[2];
        uint64_t count = std::stoull(argv[3]);
        mutation = argv[4];
        Geometry geometry;
        Metrics metrics;
        if (mode == "q5") metrics = verify5(geometry, count);
        else if (mode == "q6") metrics = verify6(geometry, count);
        else if (mode == "types6") metrics = verify_types6(geometry, count);
        else if (mode == "matrix5") metrics = verify_matrix(geometry, 5, count);
        else if (mode == "matrix6") metrics = verify_matrix(geometry, 6, count);
        else throw std::runtime_error("UNKNOWN_MODE");
        require(mutation == "none", "MUTATION_WAS_NOT_REJECTED");
        metrics["rebuilt_oriented_rhombi"] = 45;
        metrics["rebuilt_primitive_normals"] = 42;
        metrics["rebuilt_integer_orthogonal_actions"] = 6;
        struct rusage usage{}; getrusage(RUSAGE_SELF, &usage);
        std::cout << "{\"status\":\"" << (metrics["complete"] ? "PASS_COMPLETE_FINITE_PREDICATES" : "PASS_COMPLETE_PILOT_PREFIX")
                  << "\",\"mode\":" << std::quoted(mode) << ",\"elapsed_seconds\":" << std::setprecision(12) << elapsed()
                  << ",\"maximum_rss_platform_units\":" << usage.ru_maxrss << ",\"counts\":{";
        bool first = true;
        for (auto item : metrics) { if (!first) std::cout << ','; first = false; std::cout << std::quoted(item.first) << ':' << item.second; }
        std::cout << "}}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cout << "{\"status\":\"REFUSED_OR_INCOMPLETE\",\"reason\":" << std::quoted(error.what())
                  << ",\"elapsed_seconds\":" << std::setprecision(12) << elapsed() << "}\n";
        return 2;
    }
}
