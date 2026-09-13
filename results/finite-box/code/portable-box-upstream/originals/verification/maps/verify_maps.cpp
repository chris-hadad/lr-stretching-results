// Independent replay of the mathematical operations in P08 proof 029 and README.
// No provider CODE is used. This verifies maps and inventory, not LR counts,
// feasibility, chart dimension bounds, or the preceding original-box filter.
// C++17, standard library only. See README.md for input binding and partial runs.

#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

namespace fs = std::filesystem;
using U64 = std::uint64_t;
using Partition = std::array<std::uint8_t, 7>;

[[noreturn]] void fail(const std::string& message) { throw std::runtime_error(message); }
void require(bool condition, const std::string& message) { if (!condition) fail(message); }
void require(bool condition, const char* message) { if (!condition) fail(message); }

U64 add(U64 a, U64 b) {
    if (a > std::numeric_limits<U64>::max() - b) fail("unsigned counter overflow");
    return a + b;
}

struct Reader {
    fs::path path;
    std::ifstream stream;
    std::string line;
    U64 number = 0;
    explicit Reader(const fs::path& p) : path(p), stream(p, std::ios::binary) {
        require(stream.is_open(), "cannot open " + p.string());
    }
    [[noreturn]] void bad(const std::string& message) const {
        fail(path.string() + ":" + std::to_string(number) + ": " + message);
    }
    bool next() {
        if (!std::getline(stream, line)) {
            if (!stream.eof()) bad("read failed");
            return false;
        }
        number = add(number, 1);
        if (stream.eof()) bad("record must end with LF");
        if (line.empty() || line.size() > 4096) bad("empty or overlong record");
        return true;
    }
    void header(std::string_view expected) {
        if (!next() || line != expected) bad("incorrect or missing header");
    }
};

template<std::size_t N>
std::array<std::string_view, N> fields(const Reader& reader, char separator = '\t') {
    std::array<std::string_view, N> result;
    std::string_view text(reader.line);
    std::size_t start = 0;
    for (std::size_t i = 0; i < N; ++i) {
        const auto end = text.find(separator, start);
        if ((i + 1 == N) != (end == std::string_view::npos)) reader.bad("incorrect field count");
        result[i] = text.substr(start, end == std::string_view::npos ? end : end - start);
        if (result[i].empty()) reader.bad("empty field");
        if (end != std::string_view::npos) start = end + 1;
    }
    return result;
}

U64 integer(std::string_view text, const Reader& reader) {
    if (text.empty() || (text.size() > 1 && text[0] == '0')) reader.bad("noncanonical integer");
    U64 value = 0;
    const auto parsed = std::from_chars(text.data(), text.data() + text.size(), value);
    if (parsed.ec != std::errc() || parsed.ptr != text.data() + text.size())
        reader.bad("invalid or overflowing unsigned integer");
    return value;
}

struct Key {
    std::array<Partition, 3> p{};  // Full lambda, mu, nu; explicit zero padding to seven slots.
    std::uint8_t rank = 0;       // Maximum positive-part length, checked against serialized padding.
    bool operator==(const Key& other) const { return rank == other.rank && p == other.p; }
};

// Exact base-32 integer order sum(part[i] * 32^i), first part least significant.
// Compare full arrays in reverse order, avoiding both hash collisions and packing assumptions
// about machine width. The input bound part <= 30 makes this equivalent to five-bit packing.
bool partition_packed_less(const Partition& a, const Partition& b) {
    for (int i = 6; i >= 0; --i) {
        if (a[static_cast<std::size_t>(i)] != b[static_cast<std::size_t>(i)])
            return a[static_cast<std::size_t>(i)] < b[static_cast<std::size_t>(i)];
    }
    return false;
}

bool key_less(const Key& a, const Key& b) {
    if (a.rank != b.rank) return a.rank < b.rank;
    for (std::size_t i = 0; i < 3; ++i) {
        if (a.p[i] != b.p[i]) return partition_packed_less(a.p[i], b.p[i]);
    }
    return false;
}

unsigned area(const Partition& p) {
    // Seven validated entries of at most 30: this sum is bounded by 210.
    return std::accumulate(p.begin(), p.end(), 0U);
}

unsigned actual_rank(const Key& key) {
    for (unsigned n = 7; n > 0; --n) {
        for (const auto& p : key.p) if (p[n - 1] != 0) return n;
    }
    return 0;
}

std::string describe(const Key& key) {
    std::string result = "rank=" + std::to_string(key.rank);
    for (const auto& p : key.p) {
        result += " [";
        for (unsigned i = 0; i < key.rank; ++i) {
            if (i) result += ',';
            result += std::to_string(p[i]);
        }
        result += ']';
    }
    return result;
}

Partition partition(std::string_view text, unsigned n, const Reader& reader) {
    Partition result{};
    std::size_t start = 0;
    for (unsigned i = 0; i < n; ++i) {
        const auto end = text.find(',', start);
        if ((i + 1 == n) != (end == std::string_view::npos)) reader.bad("partition padding differs from rank");
        const U64 value = integer(text.substr(start, end == std::string_view::npos ? end : end - start), reader);
        if (value > 30) reader.bad("partition part exceeds the supported area-thirty box");
        result[i] = static_cast<std::uint8_t>(value);
        if (i && result[i - 1] < result[i]) reader.bad("partition is not weakly decreasing");
        if (end != std::string_view::npos) start = end + 1;
    }
    return result;
}

Key key_from(unsigned n, std::string_view l, std::string_view m, std::string_view v,
             const Reader& reader, bool original) {
    if (n != 6 && n != 7) reader.bad("unsupported actual rank; only six and seven are retained");
    Key result{{partition(l, n, reader), partition(m, n, reader), partition(v, n, reader)},
               static_cast<std::uint8_t>(n)};
    if (actual_rank(result) != n) reader.bad("recorded rank is not the actual positive-part rank");
    const unsigned lsize = area(result.p[0]), msize = area(result.p[1]), vsize = area(result.p[2]);
    if (!msize || !vsize || lsize > 30 || lsize != msize + vsize)
        reader.bad("unsupported empty, unbalanced, or out-of-box boundary");
    if (original) {
        if (result.p[2] < result.p[1]) reader.bad("original inners are not in lexicographic order");
        unsigned lp = 0, mp = 0, vp = 0;
        for (unsigned i = 0; i < n; ++i) {
            if (result.p[0][i] < result.p[1][i] || result.p[0][i] < result.p[2][i])
                reader.bad("original residual fails necessary containment");
            lp += result.p[0][i]; mp += result.p[1][i]; vp += result.p[2][i];
            if (lp > mp + vp) reader.bad("original residual fails a necessary highest-weight prefix");
        }
    } else {
        if (partition_packed_less(result.p[2], result.p[1])) reader.bad("key inners violate declared packed order");
        unsigned g = 0;
        for (const auto& p : result.p) for (auto value : p) g = std::gcd(g, static_cast<unsigned>(value));
        if (g != 1) reader.bad("evaluation key is not primitive");
    }
    return result;
}

struct Expected { U64 original6, original7, local6, local7, global, overlap, evaluation6, evaluation7; };

Expected expectations(const fs::path& path) {
    Reader reader(path);
    reader.header("name\tvalue");
    std::map<std::string, U64> data;
    while (reader.next()) {
        const auto row = fields<2>(reader);
        if (!data.emplace(std::string(row[0]), integer(row[1], reader)).second)
            reader.bad("duplicate expectation");
    }
    const std::array<std::string, 8> names = {"original6", "original7", "local6", "local7",
                                           "global", "overlap", "evaluation6", "evaluation7"};
    if (data.size() != names.size()) reader.bad("exactly eight named expectations are required");
    for (const auto& name : names) if (!data.count(name)) reader.bad("missing expectation " + name);
    Expected e{data.at("original6"), data.at("original7"), data.at("local6"), data.at("local7"),
               data.at("global"), data.at("overlap"), data.at("evaluation6"), data.at("evaluation7")};
    require(e.local6 <= e.original6 && e.local7 <= e.original7, "more local keys than original roots");
    require(e.overlap <= std::min(e.local6, e.local7), "invalid expected overlap");
    require(add(e.local6, e.local7) - e.overlap == e.global, "inconsistent expected global union");
    require(add(e.evaluation6, e.evaluation7) == e.global, "inconsistent expected evaluation ranks");
    return e;
}

struct Local { Key key; U64 declared, observed = 0, global_id; };

std::vector<Local> load_local(const fs::path& input, unsigned rank, U64 expected_rows,
                              U64 expected_originals, U64 expected_global) {
    const auto suffix = std::to_string(rank);
    Reader keys(input / ("CANON" + suffix + "-KEYS.tsv"));
    Reader joins(input / ("GLOBAL-MAP" + suffix + ".txt"));
    keys.header("id\trank\tlambda\tmu\tnu\tpreimages");
    std::vector<Local> result;
    require(expected_rows <= result.max_size(), "local roster cannot fit this address space");
    result.reserve(static_cast<std::size_t>(expected_rows));
    U64 total = 0, previous_global = 0;
    while (keys.next()) {
        const auto row = fields<6>(keys);
        if (integer(row[0], keys) != add(result.size(), 1)) keys.bad("nonconsecutive local ID");
        const U64 n = integer(row[1], keys);
        if (n != 6 && n != 7) keys.bad("unsupported local evaluation rank");
        if (n > rank) keys.bad("evaluation rank exceeds original padding rank");
        const Key key = key_from(static_cast<unsigned>(n), row[2], row[3], row[4], keys, false);
        if (!result.empty() && !key_less(result.back().key, key)) keys.bad("duplicate or reordered local identity");
        const U64 preimages = integer(row[5], keys);
        if (!preimages || preimages > expected_originals) keys.bad("invalid local preimage count");
        if (!joins.next()) joins.bad("missing local-to-global join");
        const U64 global_id = integer(joins.line, joins);
        if (global_id <= previous_global || global_id > expected_global) joins.bad("duplicate or reordered global join");
        previous_global = global_id;
        total = add(total, preimages);
        result.push_back(Local{key, preimages, 0, global_id});
        if (result.size() > expected_rows) keys.bad("extra local key");
    }
    if (joins.next()) joins.bad("extra local-to-global join");
    require(result.size() == expected_rows, "incorrect local key roster for rank " + suffix);
    require(total == expected_originals, "incorrect declared local preimage sum for rank " + suffix);
    return result;
}

struct Transformation {
    Key key;
    unsigned scale = 0;
    int a = 0, b = 0;
    bool swapped = false, negative_outer = false;
};

Transformation transform(const Key& original, unsigned variant) {
    require(variant < 6, "variant outside the documented encoding");
    const unsigned n = original.rank, dual = variant / 3, outer = variant % 3;
    using Weight = std::array<int, 7>;
    std::array<Weight, 3> weights{};
    auto star = [n](const Weight& w) {
        Weight result{};
        for (unsigned i = 0; i < n; ++i) result[i] = -w[n - 1 - i];
        return result;
    };
    for (unsigned i = 0; i < n; ++i) {
        weights[0][i] = original.p[1][i];
        weights[1][i] = original.p[2][i];
        weights[2][i] = -static_cast<int>(original.p[0][n - 1 - i]);
    }
    if (dual) for (auto& w : weights) w = star(w);
    std::array<Weight, 3> normalized = {star(weights[outer]), weights[(outer + 1) % 3],
                                      weights[(outer + 2) % 3]};
    Transformation result;
    result.a = normalized[1][n - 1]; result.b = normalized[2][n - 1];
    // All parsed parts are <= 30, signed weights lie in [-30,30], and shifts
    // lie in [-60,60]. Every operation below is in [-90,90], so signed int
    // arithmetic is safe even at the C++ minimum required 16-bit int width.
    for (unsigned i = 0; i < n; ++i) {
        normalized[0][i] -= result.a + result.b;
        normalized[1][i] -= result.a;
        normalized[2][i] -= result.b;
    }
    if (normalized[0][n - 1] < 0) { result.negative_outer = true; return result; }
    unsigned g = 0;
    for (const auto& p : normalized) {
        for (unsigned i = 0; i < n; ++i) {
            require(p[i] >= 0 && p[i] <= 30, "transformed pre-gcd part violates the proved box bound");
            require(!i || p[i - 1] >= p[i], "transformed weight is not dominant");
            g = std::gcd(g, static_cast<unsigned>(p[i]));
        }
    }
    if (!g) return result;  // The caller rejects the unsupported zero/terminal branch.
    result.scale = g;
    for (unsigned p = 0; p < 3; ++p) for (unsigned i = 0; i < n; ++i)
        result.key.p[p][i] = static_cast<std::uint8_t>(static_cast<unsigned>(normalized[p][i]) / g);
    result.key.rank = static_cast<std::uint8_t>(actual_rank(result.key));
    require(area(result.key.p[0]) == area(result.key.p[1]) + area(result.key.p[2]),
            "determinant normalization broke size balance");
    if (partition_packed_less(result.key.p[2], result.key.p[1])) {
        std::swap(result.key.p[1], result.key.p[2]); result.swapped = true;
    }
    return result;
}

bool score_less(const Key& a, const Key& b) {
    const unsigned aa = area(a.p[0]), ba = area(b.p[0]);
    return aa != ba ? aa < ba : key_less(a, b);
}

struct Stats {
    std::array<U64, 8> parsed{}, verified{}, selected_rank{};
    std::array<U64, 6> variants{};
    std::array<U64, 31> scales{};
    U64 inner_swaps = 0, rank_drops = 0;
    U64 global_rows = 0, overlap = 0, preimages6 = 0, preimages7 = 0;
    U64 evaluation6 = 0, evaluation7 = 0, small_keys = 0, small_pre6 = 0, small_pre7 = 0;
};

void replay_originals(const fs::path& input, unsigned rank, U64 expected_rows,
                      std::vector<Local>& local, U64 first, U64 last, Stats& stats) {
    const auto suffix = std::to_string(rank);
    Reader originals(input / ("BOX" + suffix + "-RESIDUAL.tsv"));
    Reader maps(input / ("CANON" + suffix + "-MAP.tsv"));
    originals.header("lambda\tmu\tnu\tchart_bound");
    maps.header("evaluation_id_or_terminal\tstretch_scale\tvariant");
    std::vector<Key> identities;
    require(expected_rows <= identities.max_size(), "original roster cannot fit this address space");
    identities.reserve(static_cast<std::size_t>(expected_rows));
    U64 row_number = 0;
    while (originals.next()) {
        row_number = add(row_number, 1);
        if (row_number > expected_rows) originals.bad("extra original root");
        const auto row = fields<4>(originals);
        const Key original = key_from(rank, row[0], row[1], row[2], originals, true);
        const U64 chart = integer(row[3], originals);
        if (chart < 4 || chart > (rank - 1) * (rank - 2) / 2)
            originals.bad("unsupported residual chart-bound annotation");
        identities.push_back(original);
        if (!maps.next()) maps.bad("missing original-to-local row");
        const auto map = fields<3>(maps);
        const U64 id = integer(map[0], maps), g = integer(map[1], maps), v = integer(map[2], maps);
        if (!id || id > local.size()) maps.bad("terminal or unknown evaluation ID");
        if (!g || g > 30 || v > 5) maps.bad("invalid stretch scale or variant");
        auto& target = local[static_cast<std::size_t>(id - 1)];
        target.observed = add(target.observed, 1);
        if (target.observed > target.declared) maps.bad("too many preimages for the named local key");
        stats.parsed[rank] = add(stats.parsed[rank], 1);
        if (row_number >= first && row_number <= last) {
            Transformation selected;
            Key minimum;
            bool have_minimum = false;
            for (unsigned variant = 0; variant < 6; ++variant) {
                const auto candidate = transform(original, variant);
                if (candidate.negative_outer || !candidate.scale || candidate.key.rank < 6)
                    originals.bad("unexpected determinant-zero or low-rank terminal at variant "
                                  + std::to_string(variant) + "; " + describe(original));
                if (variant == v) selected = candidate;
                if (area(candidate.key.p[0]) <= 30 && (!have_minimum || score_less(candidate.key, minimum))) {
                    minimum = candidate.key; have_minimum = true;
                }
            }
            if (!(selected.key == target.key) || selected.scale != g)
                originals.bad("documented variant/scale does not reach named local ID " + std::to_string(id)
                              + "; original " + describe(original) + "; transformed " + describe(selected.key)
                              + "; named " + describe(target.key) + "; computed scale="
                              + std::to_string(selected.scale) + "; recorded scale=" + std::to_string(g));
            if (!have_minimum || !(minimum == target.key))
                originals.bad("named key is not a minimum under the six documented variants; " + describe(original));
            stats.verified[rank] = add(stats.verified[rank], 1);
            stats.variants[static_cast<std::size_t>(v)] = add(stats.variants[static_cast<std::size_t>(v)], 1);
            stats.scales[static_cast<std::size_t>(g)] = add(stats.scales[static_cast<std::size_t>(g)], 1);
            stats.selected_rank[selected.key.rank] = add(stats.selected_rank[selected.key.rank], 1);
            stats.inner_swaps = add(stats.inner_swaps, selected.swapped ? 1 : 0);
            stats.rank_drops = add(stats.rank_drops, selected.key.rank < rank ? 1 : 0);
        }
        if (row_number % 500000 == 0) std::cerr << "rank " << rank << ": parsed " << row_number
                                               << ", transformed " << stats.verified[rank] << '\n';
    }
    if (maps.next()) maps.bad("extra original-to-local row");
    require(row_number == expected_rows, "missing original roots for rank " + suffix);
    for (std::size_t i = 0; i < local.size(); ++i) {
        if (local[i].observed != local[i].declared)
            fail("rank " + suffix + " local ID " + std::to_string(i + 1) + ": exact preimage mismatch");
    }
    // The input's enumeration order is frozen externally. Sorting a separate full-identity
    // vector checks uniqueness without changing the row-index joins used above.
    std::sort(identities.begin(), identities.end(), [](const Key& a, const Key& b) { return a.p < b.p; });
    for (std::size_t i = 1; i < identities.size(); ++i)
        if (identities[i - 1] == identities[i]) fail("duplicate original identity: " + describe(identities[i]));
}

void global_merge(const fs::path& input, const std::vector<Local>& six, const std::vector<Local>& seven,
                  const Expected& expected, Stats& stats) {
    Reader globals(input / "GLOBAL-KEYS.tsv");
    globals.header("id\trank\tlambda\tmu\tnu\toriginal_rank6_preimages\toriginal_rank7_preimages");
    std::size_t i6 = 0, i7 = 0;
    Key previous;
    bool have_previous = false;
    while (globals.next()) {
        const auto row = fields<7>(globals);
        const U64 id = integer(row[0], globals), n = integer(row[1], globals);
        if (id != add(stats.global_rows, 1)) globals.bad("nonconsecutive global ID");
        if (n != 6 && n != 7) globals.bad("unsupported global rank");
        const Key key = key_from(static_cast<unsigned>(n), row[2], row[3], row[4], globals, false);
        if (have_previous && !key_less(previous, key)) globals.bad("duplicate or reordered global identity");
        previous = key; have_previous = true;
        if ((i6 < six.size() && key_less(six[i6].key, key)) ||
            (i7 < seven.size() && key_less(seven[i7].key, key))) globals.bad("a local identity is missing globally");
        const bool has6 = i6 < six.size() && six[i6].key == key;
        const bool has7 = i7 < seven.size() && seven[i7].key == key;
        if (!has6 && !has7) globals.bad("global identity has no local source");
        const U64 pre6 = integer(row[5], globals), pre7 = integer(row[6], globals);
        if (pre6 != (has6 ? six[i6].observed : 0) || pre7 != (has7 ? seven[i7].observed : 0))
            globals.bad("exact rank-six/seven preimage counters disagree with original-row maps");
        if ((has6 && six[i6].global_id != id) || (has7 && seven[i7].global_id != id))
            globals.bad("local-to-global join points at a different complete identity");
        if (has6) ++i6;
        if (has7) ++i7;
        stats.overlap = add(stats.overlap, has6 && has7 ? 1 : 0);
        stats.global_rows = add(stats.global_rows, 1);
        stats.preimages6 = add(stats.preimages6, pre6); stats.preimages7 = add(stats.preimages7, pre7);
        if (n == 6) stats.evaluation6 = add(stats.evaluation6, 1);
        else stats.evaluation7 = add(stats.evaluation7, 1);
        if (area(key.p[0]) <= 16) {
            stats.small_keys = add(stats.small_keys, 1);
            stats.small_pre6 = add(stats.small_pre6, pre6); stats.small_pre7 = add(stats.small_pre7, pre7);
        }
        if (stats.global_rows > expected.global) globals.bad("extra global key");
    }
    require(i6 == six.size() && i7 == seven.size(), "global merge omitted local keys");
    require(stats.global_rows == expected.global && stats.overlap == expected.overlap,
            "global union or overlap roster mismatch");
    require(stats.evaluation6 == expected.evaluation6 && stats.evaluation7 == expected.evaluation7,
            "global actual-rank roster mismatch");
    require(stats.preimages6 == expected.original6 && stats.preimages7 == expected.original7,
            "global original-rank preimage sum mismatch");
}

std::string quoted(const std::string& text) {
    std::string result = "\"";
    const char* hex = "0123456789abcdef";
    for (char raw : text) {
        const auto c = static_cast<unsigned char>(raw);
        if (c == '\\' || c == '"') { result += '\\'; result += static_cast<char>(c); }
        else if (c < 32) { result += "\\u00"; result += hex[c >> 4]; result += hex[c & 15]; }
        else result += static_cast<char>(c);
    }
    return result + '"';
}

struct Options {
    fs::path input, output, expected;
    std::string mode = "full", binding;
    unsigned rank = 0;
    U64 first = 0, last = 0;
};

U64 option_integer(const std::string& value) {
    U64 result = 0;
    const auto parsed = std::from_chars(value.data(), value.data() + value.size(), result);
    require(!value.empty() && parsed.ec == std::errc() && parsed.ptr == value.data() + value.size(),
            "invalid integer command-line argument");
    return result;
}

Options options(int argc, char** argv) {
    Options o;
    std::map<std::string, std::string> args;
    for (int i = 1; i < argc; i += 2) {
        require(i + 1 < argc, "each option requires a value");
        require(args.emplace(argv[i], argv[i + 1]).second, "duplicate command-line option");
    }
    for (const auto& entry : args) {
        const auto& name = entry.first; const auto& value = entry.second;
        if (name == "--input") o.input = value;
        else if (name == "--output") o.output = value;
        else if (name == "--expected") o.expected = value;
        else if (name == "--mode") o.mode = value;
        else if (name == "--binding") o.binding = value;
        else if (name == "--rank") {
            const U64 n = option_integer(value);
            require(n == 6 || n == 7, "--rank must be six or seven"); o.rank = static_cast<unsigned>(n);
        } else if (name == "--first") o.first = option_integer(value);
        else if (name == "--last") o.last = option_integer(value);
        else fail("unknown option " + name);
    }
    require(!o.input.empty() && !o.output.empty() && !o.expected.empty(),
            "usage: verify_maps --input P08 --output FRESH_DIR --expected EXPECTED.tsv --binding SHA256 "
            "[--mode full|structure|rows] [--rank 6|7 --first N --last N]");
    require(o.binding.size() == 64 && o.binding.find_first_not_of("0123456789abcdef") == std::string::npos,
            "--binding must identify the caller-frozen input manifest with 64 lowercase hex characters");
    require(o.mode == "full" || o.mode == "structure" || o.mode == "rows", "invalid verification mode");
    if (o.mode == "rows") require(o.rank && o.first && o.last >= o.first, "rows mode requires a nonempty 1-based range");
    else require(!o.rank && !o.first && !o.last, "rank/range options are only valid in rows mode");
    return o;
}

void report(const Options& o, const Stats& s, const std::string& status, const std::string& error = "") {
    std::ofstream out(o.output / "report.json", std::ios::binary);
    require(out.is_open(), "cannot write report in fresh output directory");
    out << "{\n  \"status\": " << quoted(status) << ",\n  \"mode\": " << quoted(o.mode)
        << ",\n  \"source_binding_supplied_by_caller\": " << quoted(o.binding)
        << ",\n  \"input\": " << quoted(o.input.string())
        << ",\n  \"scope\": " << quoted(o.mode == "full" ? "all original transformations and all joins" :
             o.mode == "structure" ? "all identities and joins; no transformation replay" :
             "one transformation row range; global merge not checked")
        << ",\n  \"identity\": \"P_original(t)=P_key(g*t)\","
        << "\n  \"packing_order\": \"rank, then lambda/mu/nu; sum(part[i]*32^i) with first part least significant\","
        << "\n  \"variant_encoding\": \"3*dual+outer; cyclic inner successors; inner swap allowed\","
        << "\n  \"variant_tie_rule\": \"recorded variant must attain the minimum; no undocumented tie preference asserted\","
        << "\n  \"original_rank\": " << o.rank << ",\n  \"first_row\": " << o.first
        << ",\n  \"last_row\": " << o.last
        << ",\n  \"original6_parsed\": " << s.parsed[6] << ",\n  \"original7_parsed\": " << s.parsed[7]
        << ",\n  \"original6_transformations_verified\": " << s.verified[6]
        << ",\n  \"original7_transformations_verified\": " << s.verified[7]
        << ",\n  \"rank_drops\": " << s.rank_drops << ",\n  \"inner_swaps\": " << s.inner_swaps
        << ",\n  \"global_keys\": " << s.global_rows << ",\n  \"overlap\": " << s.overlap
        << ",\n  \"global_rank6_keys\": " << s.evaluation6 << ",\n  \"global_rank7_keys\": " << s.evaluation7
        << ",\n  \"global_preimages6\": " << s.preimages6 << ",\n  \"global_preimages7\": " << s.preimages7
        << ",\n  \"area_at_most_16_keys\": " << s.small_keys
        << ",\n  \"area_at_most_16_preimages6\": " << s.small_pre6
        << ",\n  \"area_at_most_16_preimages7\": " << s.small_pre7
        << ",\n  \"variant_histogram\": [";
    for (unsigned i = 0; i < 6; ++i) out << (i ? ", " : "") << s.variants[i];
    out << "],\n  \"scale_histogram_0_through_30\": [";
    for (unsigned i = 0; i <= 30; ++i) out << (i ? ", " : "") << s.scales[i];
    out << "],\n  \"error\": " << quoted(error) << "\n}\n";
    out.close(); require(!out.fail(), "failed to finish report");
}

int main(int argc, char** argv) {
    Options o;
    Stats stats;
    bool own_output = false;
    try {
        o = options(argc, argv);
        const Expected e = expectations(o.expected);
        if (o.mode == "rows") require(o.last <= (o.rank == 6 ? e.original6 : e.original7), "row range exceeds expected source roster");
        require(fs::create_directory(o.output), "output directory must be fresh");
        own_output = true;
        if (o.mode == "rows") {
            auto local = load_local(o.input, o.rank, o.rank == 6 ? e.local6 : e.local7,
                                    o.rank == 6 ? e.original6 : e.original7, e.global);
            replay_originals(o.input, o.rank, o.rank == 6 ? e.original6 : e.original7,
                             local, o.first, o.last, stats);
            require(stats.verified[o.rank] == o.last - o.first + 1, "incomplete transformation range");
        } else {
            auto six = load_local(o.input, 6, e.local6, e.original6, e.global);
            auto seven = load_local(o.input, 7, e.local7, e.original7, e.global);
            replay_originals(o.input, 6, e.original6, six, 1, o.mode == "full" ? e.original6 : 0, stats);
            replay_originals(o.input, 7, e.original7, seven, 1, o.mode == "full" ? e.original7 : 0, stats);
            global_merge(o.input, six, seven, e, stats);
            if (o.mode == "full") require(stats.verified[6] == e.original6 && stats.verified[7] == e.original7,
                                           "incomplete full transformation roster");
        }
        report(o, stats, "PASS");
        std::cout << "PASS " << o.mode << ": transformed " << stats.verified[6] << " rank-six and "
                  << stats.verified[7] << " rank-seven originals; global keys " << stats.global_rows << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        if (own_output) {
            try { report(o, stats, "FAIL", error.what()); }
            catch (const std::exception& nested) { std::cerr << "report failed: " << nested.what() << '\n'; }
        }
        return 1;
    }
}
