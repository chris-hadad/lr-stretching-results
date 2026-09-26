#pragma once
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
#include <gmpxx.h>

namespace lf {
using I = int64_t;
using W = __int128_t;
using U = __uint128_t;
using Ray = std::array<I, 8>;
using Signature = std::array<uint64_t, 4>;
constexpr I DEN = 479001600;
constexpr I VBOUND = 1000000;
constexpr I TBOUND = 1000000000000LL;
constexpr I FBOUND = 1024 * TBOUND;

inline void require(bool truth, const std::string& message) {
    if (!truth) throw std::runtime_error(message);
}
inline std::string decimal(W value) {
    if (!value) return "0";
    bool negative = value < 0;
    U x = negative ? U(-(value + 1)) + 1 : U(value);
    std::string s;
    while (x) { s.push_back(char('0' + x % 10)); x /= 10; }
    if (negative) s.push_back('-');
    std::reverse(s.begin(), s.end());
    return s;
}
inline std::string quoted(const std::string& s) {
    std::string out = "\"";
    for (unsigned char c : s) {
        if (c == '"' || c == '\\') { out.push_back('\\'); out.push_back(c); }
        else if (c == '\n') out += "\\n";
        else if (c >= 32) out.push_back(c);
    }
    return out + '"';
}
inline I narrow(W value, const std::string& label) {
    require(value >= std::numeric_limits<I>::min() && value <= std::numeric_limits<I>::max(),
            "int64 overflow: " + label);
    return I(value);
}
inline I integer(std::istream& input, const std::string& label) {
    I value;
    require(bool(input >> value), "Missing or out-of-range integer: " + label);
    return value;
}
inline I argument_integer(const std::string& text) {
    size_t used = 0;
    I value = std::stoll(text, &used);
    require(used == text.size() && !text.empty(), "Malformed integer argument");
    return value;
}
inline void eof(std::istream& stream, const std::string& label) {
    stream >> std::ws;
    require(stream.peek() == std::char_traits<char>::eof(), "Trailing input: " + label);
}
inline std::ofstream fresh(const std::filesystem::path& path, bool binary = false) {
    require(!std::filesystem::exists(path), "Output already exists: " + path.string());
    std::ofstream output(path, std::ios::out | (binary ? std::ios::binary : std::ios::openmode(0)));
    require(bool(output), "Cannot create output: " + path.string());
    return output;
}
inline void put_u64(std::ostream& out, uint64_t value) {
    unsigned char bytes[8];
    for (int i = 0; i < 8; ++i) bytes[i] = (value >> (8 * i)) & 255;
    out.write(reinterpret_cast<const char*>(bytes), 8);
    require(bool(out), "Output write failed");
}
inline void put_i64(std::ostream& out, I value) { put_u64(out, uint64_t(value)); }
inline I get_i64(std::istream& in) {
    unsigned char bytes[8];
    in.read(reinterpret_cast<char*>(bytes), 8);
    require(in.gcount() == 8, "Truncated binary integer");
    uint64_t bits = 0;
    for (int i = 0; i < 8; ++i) bits |= uint64_t(bytes[i]) << (8 * i);
    if (bits <= uint64_t(std::numeric_limits<I>::max())) return I(bits);
    return -1 - I(~bits);
}
inline I dot(const Ray& a, const Ray& b) {
    W value = 0;
    for (int i = 0; i < 8; ++i) value += W(a[i]) * b[i];
    return narrow(value, "ray dot product");
}
inline std::vector<Ray> row_forms() {
    std::vector<Ray> r(4);
    for (int i = 0; i < 3; ++i) r[i][i] = 1;
    r[3] = {-1, -1, -1, 0, 0, 0, 0, 1};
    return r;
}
inline std::vector<Ray> column_forms() {
    std::vector<Ray> c(5);
    for (int j = 0; j < 4; ++j) c[j][3 + j] = 1;
    c[4] = {0, 0, 0, -1, -1, -1, -1, 1};
    return c;
}
inline std::vector<Ray> domain() {
    std::vector<Ray> out;
    for (const auto& group : {row_forms(), column_forms()}) {
        for (size_t i = 0; i + 1 < group.size(); ++i) {
            Ray form{};
            for (int k = 0; k < 8; ++k) form[k] = group[i][k] - group[i + 1][k];
            out.push_back(form);
        }
        out.push_back(group.back());
    }
    require(out.size() == 9, "Wrong domain inequality count");
    return out;
}
inline std::vector<Ray> cuts() {
    auto rows = row_forms(), cols = column_forms();
    std::set<Ray> unique;
    for (int a = 1; a < 15; ++a) for (int b = 1; b < 31; ++b) {
        Ray h{};
        for (int i = 0; i < 4; ++i) if (a & (1 << i))
            for (int k = 0; k < 8; ++k) h[k] += rows[i][k];
        for (int j = 0; j < 5; ++j) if (b & (1 << j))
            for (int k = 0; k < 8; ++k) h[k] -= cols[j][k];
        I divisor = 0;
        for (I value : h) divisor = std::gcd(divisor, std::abs(value));
        require(divisor > 0, "Unexpected zero proper cut");
        for (I& value : h) value /= divisor;
        for (I value : h) if (value) {
            if (value < 0) for (I& x : h) x = -x;
            break;
        }
        unique.insert(h);
    }
    require(unique.size() == 210, "Wrong primitive proper-cut population");
    return {unique.begin(), unique.end()};
}
inline int actual_dimension(const Ray& ray) {
    int p = 0, n = 0;
    for (const Ray& f : row_forms()) { I x = dot(f, ray); require(x >= 0, "Negative row"); p += x > 0; }
    for (const Ray& f : column_forms()) { I x = dot(f, ray); require(x >= 0, "Negative column"); n += x > 0; }
    return p > 1 && n > 1 ? (p - 1) * (n - 1) : 0;
}
inline std::vector<Ray> balancing() {
    std::vector<Ray> out;
    // Column directions first, followed by the six row directions.
    for (auto [length, start] : {std::pair<int,int>{5, 3}, {4, 0}})
        for (int donor = 0; donor < length; ++donor)
            for (int receiver = donor + 1; receiver < length; ++receiver) {
                Ray b{};
                b[start + donor] = -1; // donor cannot be the implicit last entry
                if (receiver + 1 < length) b[start + receiver] = 1;
                out.push_back(b);
            }
    require(out.size() == 16, "Wrong balancing direction count");
    return out;
}

struct VertexSigns { Signature positive{}, negative{}, zero{}; uint16_t domain_positive = 0; };
struct State {
    char part;
    I first, last, total;
    std::vector<Ray> vertices;
    std::vector<VertexSigns> signs;
    std::vector<std::vector<int>> cells;
};
inline State read_state(const std::string& path, char part, I lo, I hi) {
    require(part == 'U' || part == 'F', "Unknown domain part");
    I nv_expected = part == 'U' ? 15565 : 2215;
    I nc_expected = part == 'U' ? 591214 : 41482;
    require(0 <= lo && lo < hi && hi <= nc_expected, "Invalid state interval");
    std::ifstream input(path);
    require(bool(input), "Cannot read state");
    I stage = integer(input, "stage"), nv = integer(input, "vertex count"), nc = integer(input, "cell count");
    require(stage == (part == 'U' ? 143 : 105) && nv == nv_expected && nc == nc_expected,
            "Unexpected complete state header");
    State s{part, lo, hi, nc, {}, {}, {}};
    auto base = domain(), proper = cuts();
    std::vector<Ray> all = base;
    all.insert(all.end(), proper.begin(), proper.end());
    std::set<Ray> distinct;
    for (I identity = 0; identity < nv; ++identity) {
        Ray v{};
        I divisor = 0;
        for (I& value : v) {
            value = integer(input, "vertex coordinate");
            require(value >= 0 && value <= VBOUND, "Vertex coordinate outside exact bound");
            divisor = std::gcd(divisor, value);
        }
        require(v[7] > 0 && divisor == 1 && distinct.insert(v).second, "Nonprimitive or duplicate vertex");
        VertexSigns signs;
        for (size_t j = 0; j < base.size(); ++j) {
            I value = dot(base[j], v);
            require(value >= 0, "Vertex outside sorted domain");
            if (value > 0) signs.domain_positive |= uint16_t(1) << j;
        }
        for (size_t j = 0; j < proper.size(); ++j) {
            I value = dot(proper[j], v);
            if (value > 0) signs.positive[j / 64] |= uint64_t(1) << (j % 64);
            if (value < 0) signs.negative[j / 64] |= uint64_t(1) << (j % 64);
        }
        for (size_t j = 0; j < all.size(); ++j)
            if (dot(all[j], v) == 0) signs.zero[j / 64] |= uint64_t(1) << (j % 64);
        s.vertices.push_back(v);
        s.signs.push_back(signs);
    }
    for (I identity = 0; identity < hi; ++identity) {
        I size = integer(input, "cell size");
        require(size >= 8 && size <= 128, "Cell size outside declared bound");
        std::vector<int> ids;
        for (I i = 0; i < size; ++i) {
            I value = integer(input, "cell vertex id");
            require(0 <= value && value < nv, "Cell vertex id out of range");
            ids.push_back(int(value));
        }
        std::sort(ids.begin(), ids.end());
        require(std::adjacent_find(ids.begin(), ids.end()) == ids.end(), "Duplicate cell vertex");
        if (identity >= lo) s.cells.push_back(std::move(ids));
    }
    if (hi == nc) eof(input, "state");
    require(I(s.cells.size()) == hi - lo, "State interval was truncated");
    return s;
}
inline Signature cell_signature(const State& s, const std::vector<int>& cell) {
    Signature positive{}, negative{};
    uint16_t interior = 0;
    for (int id : cell) {
        interior |= s.signs[id].domain_positive;
        for (int i = 0; i < 4; ++i) {
            positive[i] |= s.signs[id].positive[i];
            negative[i] |= s.signs[id].negative[i];
        }
    }
    require(interior == 511, "Cell has no strict sorted-domain center");
    for (int i = 0; i < 4; ++i) {
        uint64_t complete = i < 3 ? ~uint64_t(0) : (uint64_t(1) << 18) - 1;
        require(!(positive[i] & negative[i]), "Cell straddles a proper cut");
        require((positive[i] | negative[i]) == complete, "Cell center is on a proper cut");
    }
    return positive;
}
inline I modular_power(I base, I exp, I prime) {
    I out = 1;
    for (; exp; exp >>= 1, base = (base * base) % prime) if (exp & 1) out = (out * base) % prime;
    return out;
}
inline int rank_mod(const std::vector<Ray>& rows) {
    constexpr I prime = 1000000007;
    auto a = rows;
    for (Ray& row : a) for (I& x : row) { x %= prime; if (x < 0) x += prime; }
    int rank = 0;
    for (int col = 0; col < 8 && rank < int(a.size()); ++col) {
        int p = rank;
        while (p < int(a.size()) && !a[p][col]) ++p;
        if (p == int(a.size())) continue;
        std::swap(a[p], a[rank]);
        I inverse = modular_power(a[rank][col], prime - 2, prime);
        for (int j = col; j < 8; ++j) a[rank][j] = (a[rank][j] * inverse) % prime;
        for (int i = rank + 1; i < int(a.size()); ++i) if (a[i][col]) {
            I scale = a[i][col];
            for (int j = col; j < 8; ++j) {
                a[i][j] = (a[i][j] - (scale * a[rank][j]) % prime + prime) % prime;
            }
        }
        ++rank;
    }
    return rank;
}
inline std::vector<Ray> vertex_rows(const State& s, const std::vector<int>& ids, U mask) {
    std::vector<Ray> out;
    for (size_t i = 0; i < ids.size(); ++i) if (mask & (U(1) << i)) out.push_back(s.vertices[ids[i]]);
    return out;
}
inline int popcount(U mask) { return __builtin_popcountll(uint64_t(mask)) + __builtin_popcountll(uint64_t(mask >> 64)); }
inline int first_bit(U mask) {
    require(mask != 0, "Empty face");
    return uint64_t(mask) ? __builtin_ctzll(uint64_t(mask)) : 64 + __builtin_ctzll(uint64_t(mask >> 64));
}
inline U all_bits(size_t n) { return n == 128 ? ~U(0) : (U(1) << n) - 1; }
inline void refusal(const std::string& out, const std::string& message, I cell) {
    try {
        auto f = fresh(std::filesystem::path(out) / "REFUSAL.json");
        f << "{\"status\":\"REFUSED_OR_ADVERSE\",\"cell\":" << cell
          << ",\"message\":" << quoted(message) << ",\"complete\":false}\n";
    } catch (...) {}
}
inline double seconds(std::chrono::steady_clock::time_point start) {
    return std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
}
} // namespace lf
