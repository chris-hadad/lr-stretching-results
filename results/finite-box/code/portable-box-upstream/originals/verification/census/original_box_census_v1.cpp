// Independently authored original-box census from captured proofs 028 and 029.
// Provider residuals are expected comparison data, never generating data.
// C++17, Clang/GCC checked integer builtins, POSIX output; no external libraries.

#include <algorithm>
#include <array>
#include <cerrno>
#include <charconv>
#include <cstdint>
#include <cstring>
#include <fcntl.h>
#include <fstream>
#include <iostream>
#include <limits>
#include <set>
#include <stdexcept>
#include <string>
#include <string_view>
#include <tuple>
#include <unordered_map>
#include <unistd.h>
#include <utility>
#include <vector>

namespace {
using U64 = std::uint64_t;

struct Failure : std::runtime_error {
    std::string type;
    Failure(std::string category, const std::string& message)
        : std::runtime_error(message), type(std::move(category)) {}
};

struct Context {
    std::string stage = "options";
    std::string file;
    U64 line = 0;
};

U64 plus(U64 a, U64 b) {
    U64 result;
    if (__builtin_add_overflow(a, b, &result)) {
        throw Failure("overflow", "unsigned 64-bit counter addition");
    }
    return result;
}

void increment(U64& value) { value = plus(value, 1); }

std::string quote(const std::string& text) {
    std::string result = "\"";
    const char* hex = "0123456789abcdef";
    for (unsigned char c : text) {
        if (c == '\\' || c == '"') {
            result.push_back('\\');
            result.push_back(static_cast<char>(c));
        } else if (c < 32 || c >= 127) {
            result += "\\u00";
            result.push_back(hex[c >> 4]);
            result.push_back(hex[c & 15]);
        } else {
            result.push_back(static_cast<char>(c));
        }
    }
    return result + "\"";
}

unsigned small_integer(std::string_view token, unsigned maximum, const std::string& label) {
    unsigned value = 0;
    const auto parsed = std::from_chars(token.data(), token.data() + token.size(), value);
    if (parsed.ec != std::errc() || parsed.ptr != token.data() + token.size() || value > maximum) {
        throw Failure("input_domain", label + " must be a nonnegative integer within its limit");
    }
    return value;
}

struct Options {
    unsigned rank = 0;
    unsigned max_area = 0;
    std::string scores6, scores7, horn6, horn7, expected, output;
    std::size_t child_cache_limit = 1000000;
    bool validate_only = false;
};

Options options_from(int argc, char** argv) {
    Options result;
    std::set<std::string> seen;
    for (int i = 1; i < argc; ++i) {
        const std::string name = argv[i];
        if (!seen.insert(name).second) {
            throw Failure("input_domain", "duplicate option " + name);
        }
        if (name == "--validate-inputs-only") {
            result.validate_only = true;
            continue;
        }
        if (i + 1 == argc) {
            throw Failure("input_domain", "missing value for " + name);
        }
        const std::string value = argv[++i];
        if (name == "--rank") result.rank = small_integer(value, 7, name);
        else if (name == "--max-area") result.max_area = small_integer(value, 30, name);
        else if (name == "--scores6") result.scores6 = value;
        else if (name == "--scores7") result.scores7 = value;
        else if (name == "--horn6") result.horn6 = value;
        else if (name == "--horn7") result.horn7 = value;
        else if (name == "--expected-residual") result.expected = value;
        else if (name == "--output") result.output = value;
        else if (name == "--max-child-cache") result.child_cache_limit = small_integer(value, 4000000, name);
        else throw Failure("input_domain", "unknown option " + name);
    }
    for (const char* required : {"--rank", "--max-area", "--scores6", "--scores7",
                                  "--horn6", "--horn7", "--expected-residual", "--output"}) {
        if (!seen.count(required)) {
            throw Failure("input_domain", std::string("missing option ") + required);
        }
    }
    if ((result.rank != 6 && result.rank != 7) || result.max_area < 2) {
        throw Failure("input_domain", "rank must be 6 or 7 and max-area must be 2 through 30");
    }
    return result;
}

class FreshFile {
public:
    explicit FreshFile(const std::string& path) {
        descriptor_ = ::open(path.c_str(), O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0600);
        if (descriptor_ < 0) {
            const int saved = errno;
            throw Failure(saved == EEXIST ? "output_exists" : "io",
                          "exclusive output creation failed: " + std::string(std::strerror(saved)));
        }
    }
    ~FreshFile() { if (descriptor_ >= 0) ::close(descriptor_); }
    FreshFile(const FreshFile&) = delete;
    FreshFile& operator=(const FreshFile&) = delete;

    void line(const std::string& value) {
        const std::string bytes = value + '\n';
        std::size_t position = 0;
        while (position < bytes.size()) {
            const auto written = ::write(descriptor_, bytes.data() + position, bytes.size() - position);
            if (written < 0 && errno == EINTR) continue;
            if (written <= 0) throw Failure("io", "output write failed");
            position += static_cast<std::size_t>(written);
        }
    }

    void finish() {
        if (::fsync(descriptor_) != 0) throw Failure("io", "output fsync failed");
        const int descriptor = descriptor_;
        descriptor_ = -1;
        if (::close(descriptor) != 0) throw Failure("io", "output close failed");
    }

private:
    int descriptor_ = -1;
};

std::string token(std::ifstream& input, const std::string& label) {
    std::string result;
    if (!(input >> result)) throw Failure("input_domain", "missing " + label);
    return result;
}

void no_trailing_tokens(std::ifstream& input) {
    std::string extra;
    if (input >> extra) throw Failure("input_domain", "unexpected trailing tokens");
    if (input.bad()) throw Failure("io", "input read failure");
}

std::vector<std::uint8_t> read_scores(const std::string& path, unsigned rank, Context& context) {
    context = {"scores", path, 1};
    std::ifstream input(path);
    if (!input) throw Failure("io", "cannot open score table");
    const unsigned expected = 1U << (3 * (rank - 1));
    if (small_integer(token(input, "score count"), expected, "score count") != expected) {
        throw Failure("input_domain", "wrong complete score roster size");
    }
    const unsigned dimension = (rank - 1) * (rank - 2) / 2;
    std::vector<std::uint8_t> result;
    result.reserve(expected);
    for (unsigned i = 0; i < expected; ++i) {
        result.push_back(static_cast<std::uint8_t>(small_integer(token(input, "score"), dimension, "score")));
    }
    no_trailing_tokens(input);
    return result;
}

struct Horn {
    std::uint8_t size, I, J, K;
    std::uint8_t omit_I = 0, omit_J = 0, omit_K = 0;
};

unsigned tau_area(unsigned mask, unsigned cardinality) {
    unsigned sum = 0;
    for (unsigned bit = 0; bit < 7; ++bit) {
        if (mask & (1U << bit)) sum += bit;
    }
    return sum - cardinality * (cardinality - 1) / 2;
}

std::vector<Horn> read_horn(const std::string& path, unsigned rank, Context& context) {
    context = {"horn", path, 1};
    std::ifstream input(path);
    if (!input) throw Failure("io", "cannot open Horn roster");
    const unsigned expected = rank == 6 ? 521 : 2042;
    if (small_integer(token(input, "Horn count"), expected, "Horn count") != expected) {
        throw Failure("input_domain", "wrong authenticated Horn roster size");
    }
    const unsigned full = (1U << rank) - 1;
    std::set<std::tuple<unsigned, unsigned, unsigned, unsigned>> distinct;
    std::vector<Horn> result;
    result.reserve(expected);
    for (unsigned index = 0; index < expected; ++index) {
        context.line = index + 2;
        const unsigned r = small_integer(token(input, "Horn subset size"), rank - 1, "Horn subset size");
        const unsigned I = small_integer(token(input, "I mask"), full, "I mask");
        const unsigned J = small_integer(token(input, "J mask"), full, "J mask");
        const unsigned K = small_integer(token(input, "K mask"), full, "K mask");
        if (r == 0 || static_cast<unsigned>(__builtin_popcount(I)) != r ||
            static_cast<unsigned>(__builtin_popcount(J)) != r ||
            static_cast<unsigned>(__builtin_popcount(K)) != r ||
            tau_area(I, r) + tau_area(J, r) != tau_area(K, r)) {
            throw Failure("input_domain", "invalid Horn subset cardinalities or tau-area balance");
        }
        if (!distinct.emplace(r, I, J, K).second) {
            throw Failure("input_domain", "duplicate Horn index");
        }
        Horn h{static_cast<std::uint8_t>(r), static_cast<std::uint8_t>(I),
               static_cast<std::uint8_t>(J), static_cast<std::uint8_t>(K)};
        if (rank == 7 && (r == 1 || r == 6)) {
            h.omit_I = static_cast<std::uint8_t>(__builtin_ctz(r == 1 ? I : full ^ I));
            h.omit_J = static_cast<std::uint8_t>(__builtin_ctz(r == 1 ? J : full ^ J));
            h.omit_K = static_cast<std::uint8_t>(__builtin_ctz(r == 1 ? K : full ^ K));
        }
        result.push_back(h);  // Never reorder the supplied first-success tests.
    }
    no_trailing_tokens(input);
    return result;
}

struct Part {
    std::array<std::uint8_t, 7> values{};
    std::array<std::uint8_t, 7> prefix{};
    std::array<std::uint8_t, 128> subset{};
    std::array<const Part*, 7> omit_child{};
    U64 packed = 0;
    std::uint8_t area = 0, length = 0, zero_mask = 0;
    bool rho = false, source_outer = false;
};

U64 pack(const std::array<std::uint8_t, 7>& parts, unsigned rank) {
    U64 result = 0;
    for (unsigned i = 0; i < rank; ++i) result = (result << 5) | parts[i];
    return result;  // At most seven 5-bit values: exactly within 35 bits.
}

Part make_part(const std::array<std::uint8_t, 7>& values, unsigned rank, unsigned area) {
    Part part;
    part.values = values;
    part.area = static_cast<std::uint8_t>(area);
    part.packed = pack(values, rank);
    unsigned prefix = 0;
    for (unsigned i = 0; i < rank; ++i) {
        prefix += values[i];
        part.prefix[i] = static_cast<std::uint8_t>(prefix);
        if (values[i] != 0) part.length = static_cast<std::uint8_t>(i + 1);
        if (i + 1 < rank && values[i] == values[i + 1]) part.zero_mask |= 1U << i;
    }
    if (prefix != area || area > 30) throw Failure("internal", "partition area invariant failed");
    for (unsigned mask = 1; mask < (1U << rank); ++mask) {
        const unsigned bit = static_cast<unsigned>(__builtin_ctz(mask));
        part.subset[mask] = static_cast<std::uint8_t>(part.subset[mask & (mask - 1)] + values[bit]);
    }
    const std::array<std::uint8_t, 7> rho = {5, 4, 3, 2, 1, 0, 0};
    part.rho = values == rho;
    if (rank == 6) {
        part.source_outer = area == 30 && part.length == 6 && part.zero_mask == 0;
    } else {
        const std::array<std::uint8_t, 7> d13a = {9, 6, 5, 4, 3, 2, 1};
        const std::array<std::uint8_t, 7> d13b = {8, 7, 5, 4, 3, 2, 1};
        part.source_outer = values == d13a || values == d13b;
    }
    return part;
}

struct Catalog {
    std::array<std::vector<Part>, 31> by_area;
    std::array<std::vector<const Part*>, 31> all;
    std::array<std::vector<const Part*>, 31> exact_rank;
};

void partitions(unsigned remaining, unsigned maximum, unsigned depth, unsigned rank,
                unsigned total, std::array<std::uint8_t, 7>& values, std::vector<Part>& out) {
    if (remaining == 0) {
        for (unsigned i = depth; i < 7; ++i) values[i] = 0;
        out.push_back(make_part(values, rank, total));
        return;
    }
    if (depth == rank) return;
    const unsigned slots = rank - depth;
    const unsigned minimum = (remaining + slots - 1) / slots;
    const unsigned upper = std::min(remaining, maximum);
    if (upper < minimum) return;
    for (unsigned next = upper;; --next) {
        values[depth] = static_cast<std::uint8_t>(next);
        partitions(remaining - next, next, depth + 1, rank, total, values, out);
        if (next == minimum) break;
    }
}

void fill_catalog(Catalog& catalog, unsigned rank, unsigned max_area) {
    for (unsigned area = 0; area <= max_area; ++area) {
        std::array<std::uint8_t, 7> values{};
        partitions(area, area, 0, rank, area, values, catalog.by_area[area]);
    }
    // Freeze vector storage before installing any partition pointers.
    for (unsigned area = 0; area <= max_area; ++area) {
        for (const Part& part : catalog.by_area[area]) {
            catalog.all[area].push_back(&part);
            if (part.length == rank) catalog.exact_rank[area].push_back(&part);
        }
    }
}

void attach_children(Catalog& seven, const Catalog& six, unsigned max_area) {
    std::unordered_map<U64, const Part*> lookup;
    for (unsigned area = 0; area <= max_area; ++area) {
        for (const Part& part : six.by_area[area]) lookup.emplace(part.packed, &part);
    }
    for (unsigned area = 0; area <= max_area; ++area) {
        for (Part& part : seven.by_area[area]) {
            for (unsigned omitted = 0; omitted < 7; ++omitted) {
                std::array<std::uint8_t, 7> values{};
                unsigned position = 0;
                for (unsigned j = 0; j < 7; ++j) if (j != omitted) values[position++] = part.values[j];
                const auto found = lookup.find(pack(values, 6));
                if (found == lookup.end()) throw Failure("internal", "complete six-coordinate child missing");
                part.omit_child[omitted] = found->second;
            }
        }
    }
}

unsigned score(const Part& L, const Part& M, const Part& N, unsigned rank,
               const std::vector<std::uint8_t>& scores) {
    const unsigned shift = rank - 1;
    return scores[L.zero_mask | (unsigned(M.zero_mask) << shift) | (unsigned(N.zero_mask) << (2 * shift))];
}

bool basic_zero(const Part& L, const Part& M, const Part& N, unsigned rank) {
    for (unsigned i = 0; i < rank; ++i) {
        if (L.values[i] < M.values[i] || L.values[i] < N.values[i] ||
            L.prefix[i] > unsigned(M.prefix[i]) + N.prefix[i]) return true;
    }
    return false;
}

struct Key {
    U64 L, M, N;
    bool operator==(const Key& other) const { return L == other.L && M == other.M && N == other.N; }
};

// Hash arithmetic is intentionally modulo 2^64 and carries no mathematical
// count. Collision resolution always compares the complete three-part key.
U64 mix(U64 value) {
    value ^= value >> 30;
    value *= UINT64_C(0xbf58476d1ce4e5b9);
    value ^= value >> 27;
    value *= UINT64_C(0x94d049bb133111eb);
    return value ^ (value >> 31);
}

struct KeyHash {
    std::size_t operator()(const Key& key) const {
        return static_cast<std::size_t>(mix(key.L) ^ mix(key.M + UINT64_C(0x9e3779b97f4a7c15)) ^
                                        mix(key.N + UINT64_C(0x243f6a8885a308d3)));
    }
};

Key identity(const Part& L, const Part& M, const Part& N) {
    return {L.packed, std::min(M.packed, N.packed), std::max(M.packed, N.packed)};
}

std::string csv(U64 packed, unsigned rank) {
    std::string result;
    for (unsigned i = 0; i < rank; ++i) {
        const unsigned value = static_cast<unsigned>((packed >> (5 * (rank - 1 - i))) & 31);
        if (i != 0) result += ',';
        result += std::to_string(value);
    }
    return result;
}

std::string key_json(const Key& key, unsigned rank) {
    return "\"lambda\":" + quote(csv(key.L, rank)) + ",\"mu\":" + quote(csv(key.M, rank)) +
           ",\"nu\":" + quote(csv(key.N, rank));
}

struct ChildWork { U64 queries = 0, cache_hits = 0, resolved = 0, unresolved = 0; };

class ChildTerminal {
public:
    ChildTerminal(const std::vector<std::uint8_t>& scores, const std::vector<Horn>& horn,
                  std::size_t cache_limit) : scores_(scores), horn_(horn), cache_limit_(cache_limit) {}

    bool terminal(const Part& L, const Part& M, const Part& N) {
        increment(work.queries);
        if (L.area != unsigned(M.area) + N.area) throw Failure("internal", "unbalanced rank-six Horn child");
        bool result;
        if (std::max({L.length, M.length, N.length}) <= 5 || score(L, M, N, 6, scores_) <= 3 ||
            basic_zero(L, M, N, 6) || (M.rho && N.rho && L.source_outer)) {
            result = true;
        } else {
            // Preserve child orientation in the memo key. No unproved
            // equivalence of incomplete/ordered Horn test rosters is needed.
            const Key key{L.packed, M.packed, N.packed};
            const auto cached = cache_.find(key);
            if (cached != cache_.end()) {
                increment(work.cache_hits);
                result = cached->second;
            } else {
                result = false;
                for (const Horn& h : horn_) {
                    const unsigned rhs = unsigned(M.subset[h.I]) + N.subset[h.J];
                    // Negative slack proves zero; tightness has two proper
                    // rank-at-most-five children. Both certify sign only.
                    if (rhs <= L.subset[h.K]) { result = true; break; }
                }
                if (cache_.size() < cache_limit_) cache_.emplace(key, result);
            }
        }
        increment(result ? work.resolved : work.unresolved);
        return result;
    }

    std::size_t cache_size() const { return cache_.size(); }
    ChildWork work;

private:
    const std::vector<std::uint8_t>& scores_;
    const std::vector<Horn>& horn_;
    std::size_t cache_limit_;
    std::unordered_map<Key, bool, KeyHash> cache_;
};

struct Expected {
    Key key;
    std::uint32_t line;
    std::uint8_t bound;
    bool matched = false;
};

Part parse_partition(std::string_view text, unsigned rank) {
    std::array<std::uint8_t, 7> values{};
    std::size_t begin = 0;
    unsigned area = 0;
    for (unsigned i = 0; i < rank; ++i) {
        const auto end = text.find(',', begin);
        if ((i + 1 < rank && end == std::string_view::npos) ||
            (i + 1 == rank && end != std::string_view::npos)) {
            throw Failure("input_domain", "partition must have exactly rank padded entries");
        }
        const auto value = small_integer(text.substr(begin, end == std::string_view::npos ? end : end - begin),
                                         30, "partition part");
        if (i != 0 && value > values[i - 1]) throw Failure("input_domain", "partition is not weakly decreasing");
        values[i] = static_cast<std::uint8_t>(value);
        area += value;
        if (area > 30) throw Failure("input_domain", "partition area exceeds thirty");
        begin = end == std::string_view::npos ? text.size() : end + 1;
    }
    // Expected rows only need their complete identity and domain checks.
    // Do not build enumeration subset tables from comparison data.
    Part result;
    result.values = values;
    result.packed = pack(values, rank);
    result.area = static_cast<std::uint8_t>(area);
    for (unsigned i = 0; i < rank; ++i) {
        if (values[i] != 0) result.length = static_cast<std::uint8_t>(i + 1);
    }
    return result;
}

class ExpectedSet {
public:
    void load(const std::string& path, unsigned rank, unsigned max_area, Context& context) {
        context = {"expected_residual", path, 1};
        std::ifstream input(path);
        if (!input) throw Failure("io", "cannot open expected residual TSV");
        std::string line;
        if (!std::getline(input, line)) throw Failure("input_domain", "missing expected residual header");
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (line != "lambda\tmu\tnu\tchart_bound") throw Failure("input_domain", "wrong expected residual header");
        entries.reserve(rank == 6 ? 2000000 : 4000000);
        while (std::getline(input, line)) {
            increment(context.line);
            if (!line.empty() && line.back() == '\r') line.pop_back();
            std::array<std::string_view, 4> fields;
            std::size_t begin = 0;
            const std::string_view view(line);
            for (unsigned i = 0; i < 4; ++i) {
                const auto end = view.find('\t', begin);
                if ((i < 3 && end == std::string_view::npos) || (i == 3 && end != std::string_view::npos)) {
                    throw Failure("input_domain", "expected residual row requires exactly four TSV fields");
                }
                fields[i] = view.substr(begin, end == std::string_view::npos ? end : end - begin);
                begin = end == std::string_view::npos ? view.size() : end + 1;
            }
            const Part L = parse_partition(fields[0], rank);
            const Part M = parse_partition(fields[1], rank);
            const Part N = parse_partition(fields[2], rank);
            const unsigned bound = small_integer(fields[3], (rank - 1) * (rank - 2) / 2, "chart bound");
            if (M.area == 0 || N.area == 0 || L.area != unsigned(M.area) + N.area ||
                L.area > max_area || std::max({L.length, M.length, N.length}) != rank) {
                throw Failure("input_domain", "expected residual identity is outside the exact original box");
            }
            if (entries.size() >= 10000000) throw Failure("input_domain", "expected TSV exceeds 10000000 rows");
            entries.push_back({identity(L, M, N), static_cast<std::uint32_t>(context.line),
                               static_cast<std::uint8_t>(bound), false});
        }
        if (input.bad()) throw Failure("io", "expected residual read failure");
        std::size_t capacity = 1;
        while (capacity < entries.size() * 2) capacity <<= 1;
        slots_.assign(capacity, 0);
        for (std::size_t index = 0; index < entries.size(); ++index) {
            const auto location = locate(entries[index].key);
            if (slots_[location] != 0) {
                const Expected& previous = entries[slots_[location] - 1];
                context.line = entries[index].line;
                throw Failure("duplicate_expected", "duplicate full identity after inner exchange; first line " +
                              std::to_string(previous.line) + "; " + key_json(entries[index].key, rank));
            }
            slots_[location] = static_cast<std::uint32_t>(index + 1);
        }
    }

    Expected* find(const Key& key) {
        const auto index = slots_[locate(key)];
        return index == 0 ? nullptr : &entries[index - 1];
    }

    std::vector<Expected> entries;

private:
    std::size_t locate(const Key& key) const {
        const std::size_t mask = slots_.size() - 1;
        std::size_t location = KeyHash{}(key) & mask;
        while (slots_[location] != 0 && !(entries[slots_[location] - 1].key == key)) {
            location = (location + 1) & mask;
        }
        return location;
    }
    std::vector<std::uint32_t> slots_;
};

enum Branch : unsigned { MASK, BASIC_ZERO, SOURCE, HORN_NEGATIVE, HORN_SIGN, RETAINED, BRANCHES };
const std::array<const char*, BRANCHES> branch_names = {
    "mask_terminal", "basic_zero", "supplied_A004_source", "negative_horn_slack", "tight_horn_sign_terminal", "retained"
};

struct Counts {
    std::array<U64, BRANCHES> branches{};
    U64 total = 0;
    void record(Branch branch) { increment(total); increment(branches[branch]); }
};

struct Comparison { U64 matched = 0, missing_expected = 0, extra_expected = 0, bound_mismatch = 0; };

void compare_retained(const Part& L, const Part& M, const Part& N, unsigned bound,
                      unsigned rank, ExpectedSet& expected, Comparison& comparison, FreshFile& evidence) {
    const Key key = identity(L, M, N);
    Expected* row = expected.find(key);
    if (row == nullptr) {
        increment(comparison.missing_expected);
        evidence.line("{\"type\":\"generated_identity_missing_from_expected\"," + key_json(key, rank) +
                      ",\"generated_bound\":" + std::to_string(bound) + "}");
        return;
    }
    if (row->matched) throw Failure("internal", "duplicate generated full identity: " + key_json(key, rank));
    row->matched = true;
    increment(comparison.matched);
    if (row->bound != bound) {
        increment(comparison.bound_mismatch);
        evidence.line("{\"type\":\"bound_mismatch\"," + key_json(key, rank) +
                      ",\"expected_line\":" + std::to_string(row->line) +
                      ",\"expected_bound\":" + std::to_string(row->bound) +
                      ",\"generated_bound\":" + std::to_string(bound) + "}");
    }
}

std::string counts_json(const Counts& counts) {
    U64 sum = 0;
    std::string result = "{\"total\":" + std::to_string(counts.total);
    for (unsigned branch = 0; branch < BRANCHES; ++branch) {
        sum = plus(sum, counts.branches[branch]);
        result += "," + quote(branch_names[branch]) + ":" + std::to_string(counts.branches[branch]);
    }
    if (sum != counts.total) throw Failure("internal", "branch sum does not equal domain total");
    return result + ",\"horn_sign_union\":" +
           std::to_string(plus(counts.branches[HORN_NEGATIVE], counts.branches[HORN_SIGN])) + "}";
}

Branch classify_after_mask(const Part& L, const Part& M, const Part& N, unsigned rank,
                           const std::array<std::uint8_t, 7>& containment,
                           const std::array<std::uint8_t, 7>& prefix_limit,
                           bool source_pair, const std::vector<Horn>& horn, ChildTerminal& child) {
    for (unsigned i = 0; i < rank; ++i) {
        if (L.values[i] < containment[i] || L.prefix[i] > prefix_limit[i]) return BASIC_ZERO;
    }
    if (source_pair && L.source_outer) return SOURCE;
    for (const Horn& h : horn) {
        const unsigned rhs = unsigned(M.subset[h.I]) + N.subset[h.J];
        const unsigned lhs = L.subset[h.K];
        if (rhs < lhs) return HORN_NEGATIVE;
        if (rhs != lhs) continue;
        if (rank == 6 || (h.size != 1 && h.size != 6)) return HORN_SIGN;
        const Part& child_L = *L.omit_child[h.omit_K];
        const Part& child_M = *M.omit_child[h.omit_I];
        const Part& child_N = *N.omit_child[h.omit_J];
        if (child.terminal(child_L, child_M, child_N)) return HORN_SIGN;
        // An unresolved six-coordinate child does not settle the parent;
        // continue through the remaining supplied Horn indices in order.
    }
    return RETAINED;
}
}  // namespace

int main(int argc, char** argv) {
    Context context;
    try {
        if (argc == 2 && std::string(argv[1]) == "--help") {
            std::cout << "Usage: original_box_census_v1 --rank 6|7 --max-area 30 "
                         "--scores6 FILE --scores7 FILE --horn6 FILE --horn7 FILE "
                         "--expected-residual TSV --output FRESH_JSON "
                         "[--max-child-cache N] [--validate-inputs-only]\n";
            return 0;
        }
        const Options options = options_from(argc, argv);
        context = {"output", options.output, 0};
        FreshFile output(options.output);
        const std::string mismatch_path = options.output + ".mismatches.jsonl";
        context.file = mismatch_path;
        FreshFile evidence(mismatch_path);
        const auto scores6 = read_scores(options.scores6, 6, context);
        const auto scores7 = read_scores(options.scores7, 7, context);
        const auto horn6 = read_horn(options.horn6, 6, context);
        const auto horn7 = read_horn(options.horn7, 7, context);
        ExpectedSet expected;
        expected.load(options.expected, options.rank, options.max_area, context);
        if (options.validate_only) {
            output.line("{\"status\":\"inputs_validated_only\",\"enumeration_performed\":false,"
                        "\"native_calls\":0,\"rank\":" + std::to_string(options.rank) +
                        ",\"expected_rows\":" + std::to_string(expected.entries.size()) + "}");
            evidence.finish();
            output.finish();
            std::cout << "{\"status\":\"inputs_validated_only\",\"enumeration_performed\":false}\n";
            return 0;
        }

        context = {"independent_partition_generation", "", 0};
        Catalog six, seven;
        fill_catalog(six, 6, options.max_area);
        if (options.rank == 7) {
            fill_catalog(seven, 7, options.max_area);
            attach_children(seven, six, options.max_area);
        }
        const Catalog& catalog = options.rank == 6 ? six : seven;
        const auto& scores = options.rank == 6 ? scores6 : scores7;
        const auto& horn = options.rank == 6 ? horn6 : horn7;
        ChildTerminal child(scores6, horn6, options.child_cache_limit);
        std::array<Counts, 31> per_area;
        Counts total;
        Comparison comparison;
        context.stage = "complete_original_box_enumeration";
        const unsigned shift = options.rank - 1;
        for (unsigned area = 2; area <= options.max_area; ++area) {
            context.line = area;  // The active area, not a source-file line.
            Counts& counts = per_area[area];
            for (unsigned inner_area = 1; 2 * inner_area <= area; ++inner_area) {
                const unsigned other_area = area - inner_area;
                const auto& inners_M = catalog.by_area[inner_area];
                const auto& inners_N = catalog.by_area[other_area];
                for (std::size_t i = 0; i < inners_M.size(); ++i) {
                    const Part& M = inners_M[i];
                    const std::size_t first_j = inner_area == other_area ? i : 0;
                    for (std::size_t j = first_j; j < inners_N.size(); ++j) {
                        const Part& N = inners_N[j];
                        // Size-first orientation; equal-area partitions are
                        // generated decreasing lexicographically, with i<=j.
                        // Thus equal-area M>=N; comparison keys use min/max.
                        const auto& outers = std::max(M.length, N.length) == options.rank
                            ? catalog.all[area] : catalog.exact_rank[area];
                        const unsigned inner_masks = (unsigned(M.zero_mask) << shift) |
                                                     (unsigned(N.zero_mask) << (2 * shift));
                        std::array<std::uint8_t, 7> containment{}, prefix_limit{};
                        for (unsigned k = 0; k < options.rank; ++k) {
                            containment[k] = std::max(M.values[k], N.values[k]);
                            prefix_limit[k] = static_cast<std::uint8_t>(M.prefix[k] + N.prefix[k]);
                        }
                        const bool source_pair = M.rho && N.rho;
                        for (const Part* outer : outers) {
                            const Part& L = *outer;
                            const unsigned bound = scores[inner_masks | L.zero_mask];
                            const Branch branch = bound <= 3 ? MASK : classify_after_mask(
                                L, M, N, options.rank, containment, prefix_limit, source_pair, horn, child);
                            counts.record(branch);
                            if (branch == RETAINED) compare_retained(L, M, N, bound, options.rank,
                                                                    expected, comparison, evidence);
                        }
                    }
                }
            }
            total.total = plus(total.total, counts.total);
            for (unsigned branch = 0; branch < BRANCHES; ++branch) {
                total.branches[branch] = plus(total.branches[branch], counts.branches[branch]);
            }
        }
        context = {"complete_expected_set_comparison", options.expected, 0};
        for (const Expected& row : expected.entries) {
            if (!row.matched) {
                increment(comparison.extra_expected);
                evidence.line("{\"type\":\"expected_identity_not_retained_by_enumeration\"," +
                              key_json(row.key, options.rank) + ",\"expected_line\":" + std::to_string(row.line) +
                              ",\"expected_bound\":" + std::to_string(row.bound) + "}");
            }
        }
        if (plus(comparison.matched, comparison.missing_expected) != total.branches[RETAINED] ||
            plus(comparison.matched, comparison.extra_expected) != expected.entries.size()) {
            throw Failure("internal", "complete identity comparison accounting mismatch");
        }
        const bool matched = comparison.missing_expected == 0 && comparison.extra_expected == 0 &&
                             comparison.bound_mismatch == 0;
        std::string report = "{\"schema_version\":1,\"status\":" + quote(matched ? "complete" : "mismatch") +
            ",\"enumeration_performed\":true,\"native_calls\":0,\"rank\":" + std::to_string(options.rank) +
            ",\"max_area\":" + std::to_string(options.max_area) +
            ",\"production_area_30\":" + std::string(options.max_area == 30 ? "true" : "false") +
            ",\"residual_exact_match\":" + std::string(matched ? "true" : "false") +
            ",\"expected_rows\":" + std::to_string(expected.entries.size()) +
            ",\"matched_identities\":" + std::to_string(comparison.matched) +
            ",\"missing_expected_identities\":" + std::to_string(comparison.missing_expected) +
            ",\"extra_expected_identities\":" + std::to_string(comparison.extra_expected) +
            ",\"bound_mismatches\":" + std::to_string(comparison.bound_mismatch) +
            ",\"mismatch_evidence\":" + quote(mismatch_path) + ",\"totals\":" + counts_json(total) +
            ",\"per_area\":[";
        for (unsigned area = 2; area <= options.max_area; ++area) {
            if (area != 2) report += ',';
            report += "{\"area\":" + std::to_string(area) + ",\"counts\":" + counts_json(per_area[area]) +
                      ",\"partitions_at_most_rank\":" + std::to_string(catalog.by_area[area].size()) +
                      ",\"partitions_exact_rank\":" + std::to_string(catalog.exact_rank[area].size()) + "}";
        }
        report += "],\"rank6_child_checks\":{\"queries\":" + std::to_string(child.work.queries) +
                  ",\"resolved\":" + std::to_string(child.work.resolved) +
                  ",\"unresolved\":" + std::to_string(child.work.unresolved) +
                  ",\"cache_hits\":" + std::to_string(child.work.cache_hits) +
                  ",\"cache_entries\":" + std::to_string(child.cache_size()) + "}}";
        evidence.finish();
        output.line(report);
        output.finish();
        std::cout << "{\"status\":" << quote(matched ? "complete" : "mismatch")
                  << ",\"residual_exact_match\":" << (matched ? "true" : "false") << "}\n";
        return matched ? 0 : 2;
    } catch (const Failure& error) {
        std::cerr << "{\"status\":\"failed\",\"error_type\":" << quote(error.type)
                  << ",\"message\":" << quote(error.what()) << ",\"stage\":" << quote(context.stage)
                  << ",\"file\":" << quote(context.file) << ",\"line_or_area\":" << context.line << "}\n";
        return 1;
    } catch (const std::exception& error) {
        std::cerr << "{\"status\":\"failed\",\"error_type\":\"internal\",\"message\":" << quote(error.what())
                  << ",\"stage\":" << quote(context.stage) << "}\n";
        return 1;
    }
}
