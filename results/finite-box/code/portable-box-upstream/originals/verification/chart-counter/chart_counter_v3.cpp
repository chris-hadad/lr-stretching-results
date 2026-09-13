// Exact integer points in a complete bounded homogeneous H-polytope, d <= 5.
// Rows are c*t + sum(a_i*x_i) >= 0. All input coefficients are signed int64.
// Compile with Clang/GCC, C++17. No external libraries or counting engines.

#include <algorithm>
#include <array>
#include <cerrno>
#include <charconv>
#include <cstdint>
#include <cstring>
#include <fcntl.h>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <unistd.h>
#include <utility>
#include <vector>

namespace {
using Int = __int128_t;
using Row = std::array<Int, 6>;  // constant, then x_0, ..., x_4
using System = std::vector<Row>;

struct Failure : std::runtime_error {
    std::string type;
    Failure(std::string category, const std::string& message)
        : std::runtime_error(message), type(std::move(category)) {}
};

Int add(Int a, Int b) {
    Int result;
    if (__builtin_add_overflow(a, b, &result)) {
        throw Failure("overflow", "signed 128-bit addition");
    }
    return result;
}

Int sub(Int a, Int b) {
    Int result;
    if (__builtin_sub_overflow(a, b, &result)) {
        throw Failure("overflow", "signed 128-bit subtraction");
    }
    return result;
}

Int mul(Int a, Int b) {
    Int result;
    if (__builtin_mul_overflow(a, b, &result)) {
        throw Failure("overflow", "signed 128-bit multiplication");
    }
    return result;
}

Int neg(Int a) { return sub(0, a); }
Int absolute(Int a) { return a < 0 ? neg(a) : a; }

Int gcd(Int a, Int b) {
    while (b != 0) {
        const Int remainder = a % b;
        a = b;
        b = remainder;
    }
    return a;
}

Int floor_div(Int a, Int positive_denominator) {
    if (positive_denominator <= 0) {
        throw Failure("internal", "nonpositive floor denominator");
    }
    const Int quotient = a / positive_denominator;
    return a % positive_denominator < 0 ? sub(quotient, 1) : quotient;
}

Int ceil_div(Int a, Int positive_denominator) {
    if (positive_denominator <= 0) {
        throw Failure("internal", "nonpositive ceiling denominator");
    }
    const Int quotient = a / positive_denominator;
    return a % positive_denominator > 0 ? add(quotient, 1) : quotient;
}

std::string decimal(Int value) {
    const bool negative = value < 0;
    // This form also formats the most negative signed value without negation.
    __uint128_t magnitude = negative
        ? static_cast<__uint128_t>(-(value + 1)) + 1
        : static_cast<__uint128_t>(value);
    std::string result;
    do {
        result.push_back(static_cast<char>('0' + magnitude % 10));
        magnitude /= 10;
    } while (magnitude != 0);
    if (negative) {
        result.push_back('-');
    }
    std::reverse(result.begin(), result.end());
    return result;
}

std::string quote(const std::string& value) {
    std::string result = "\"";
    const char* hex = "0123456789abcdef";
    for (unsigned char c : value) {
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

std::int64_t integer64(const std::string& token, const std::string& label) {
    std::int64_t value = 0;
    const auto parsed = std::from_chars(token.data(), token.data() + token.size(), value);
    if (parsed.ec != std::errc() || parsed.ptr != token.data() + token.size()) {
        throw Failure("input_domain", label + " must be a signed 64-bit decimal integer");
    }
    return value;
}

std::int64_t bounded_integer(const std::string& token, const std::string& label,
                             std::int64_t low, std::int64_t high) {
    const auto value = integer64(token, label);
    if (value < low || value > high) {
        throw Failure("input_domain", label + " outside supported range");
    }
    return value;
}

struct Limits {
    std::uint64_t fm_pairs = 2000000;
    std::size_t projected_rows = 50000;
    std::uint64_t search_nodes = 10000000;
};

struct Options {
    std::string input;
    std::string output;
    std::size_t start = 0;
    std::size_t stop = 0;
    std::vector<std::int64_t> nodes;
    Limits limits;
    bool cache = true;
};

Options parse_options(int argc, char** argv) {
    Options options;
    std::set<std::string> seen;
    for (int i = 1; i < argc; ++i) {
        const std::string name = argv[i];
        if (!seen.insert(name).second) {
            throw Failure("input_domain", "duplicate option " + name);
        }
        if (name == "--no-cache") {
            options.cache = false;
            continue;
        }
        if (i + 1 == argc) {
            throw Failure("input_domain", "missing option value for " + name);
        }
        const std::string value = argv[++i];
        if (name == "--input") {
            options.input = value;
        } else if (name == "--output") {
            options.output = value;
        } else if (name == "--start") {
            options.start = bounded_integer(value, name, 0, 100000);
        } else if (name == "--stop") {
            options.stop = bounded_integer(value, name, 0, 100000);
        } else if (name == "--max-fm-pairs") {
            options.limits.fm_pairs = bounded_integer(value, name, 0, 1000000000000LL);
        } else if (name == "--max-projected-rows") {
            options.limits.projected_rows = bounded_integer(value, name, 1, 100000);
        } else if (name == "--max-search-nodes") {
            options.limits.search_nodes = bounded_integer(value, name, 0, 1000000000000LL);
        } else if (name == "--nodes") {
            std::set<std::int64_t> distinct;
            std::size_t begin = 0;
            do {
                const auto end = value.find(',', begin);
                const auto token = value.substr(begin, end == std::string::npos ? end : end - begin);
                const auto node = integer64(token, "dilation node");
                if (node < 0 || !distinct.insert(node).second) {
                    throw Failure("input_domain", "dilation nodes must be nonnegative and distinct");
                }
                options.nodes.push_back(node);
                if (options.nodes.size() > 256) {
                    throw Failure("input_domain", "at most 256 dilation nodes per launch");
                }
                if (end == std::string::npos) {
                    break;
                }
                begin = end + 1;
            } while (true);
        } else {
            throw Failure("input_domain", "unknown option " + name);
        }
    }
    for (const auto* required : {"--input", "--output", "--start", "--stop", "--nodes"}) {
        if (!seen.count(required)) {
            throw Failure("input_domain", std::string("missing option ") + required);
        }
    }
    if (options.start >= options.stop) {
        throw Failure("input_domain", "require start < stop");
    }
    return options;
}

bool normalize(Row& row) {
    Int divisor = 0;
    for (Int entry : row) {
        divisor = gcd(divisor, absolute(entry));
    }
    if (divisor == 0) {
        return false;  // The all-zero inequality is identically true.
    }
    for (Int& entry : row) {
        entry /= divisor;  // Positive division only: never reverse a sign.
    }
    return true;
}

System canonical(System rows) {
    System result;
    for (Row row : rows) {
        if (normalize(row)) {
            result.push_back(row);
        }
    }
    std::sort(result.begin(), result.end());
    result.erase(std::unique(result.begin(), result.end()), result.end());
    return result;
}

struct Record {
    std::string id;
    int dimension;
    std::size_t input_rows;
    System rows;
};

std::string next_token(std::ifstream& input, const std::string& label) {
    std::string token;
    if (!(input >> token)) {
        throw Failure("input_domain", "missing token for " + label);
    }
    return token;
}

std::vector<Record> read_records(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw Failure("io", "cannot open input file");
    }
    const auto count = bounded_integer(next_token(input, "record count"), "record count", 1, 100000);
    std::vector<Record> records;
    records.reserve(static_cast<std::size_t>(count));
    std::set<std::string> ids;
    std::size_t total_rows = 0;
    for (std::int64_t index = 0; index < count; ++index) {
        Record record;
        record.id = next_token(input, "record id");
        if (record.id.size() > 128 || !ids.insert(record.id).second ||
            !std::all_of(record.id.begin(), record.id.end(), [](unsigned char c) {
                return c >= 33 && c <= 126;
            })) {
            throw Failure("input_domain", "record ids must be unique printable ASCII tokens of at most 128 bytes");
        }
        record.dimension = static_cast<int>(bounded_integer(
            next_token(input, "dimension"), "dimension", 0, 5));
        record.input_rows = static_cast<std::size_t>(bounded_integer(
            next_token(input, "row count"), "row count", 0, 4096));
        total_rows += record.input_rows;
        if (total_rows > 2000000) {
            throw Failure("input_domain", "input exceeds 2000000 total rows");
        }
        for (std::size_t r = 0; r < record.input_rows; ++r) {
            Row row{};
            for (int j = 0; j <= record.dimension; ++j) {
                row[j] = integer64(next_token(input, "row coefficient"), "row coefficient");
            }
            record.rows.push_back(row);
        }
        record.rows = canonical(std::move(record.rows));
        records.push_back(std::move(record));
    }
    std::string trailing;
    if (input >> trailing) {
        throw Failure("input_domain", "unexpected tokens after declared records");
    }
    if (input.bad()) {
        throw Failure("io", "input read failure");
    }
    return records;
}

struct ProjectionWork {
    std::uint64_t pairs = 0;
    std::size_t peak_rows = 0;
};

void insert_row(std::map<Row, Row>& rows, Row row, const Limits& limits,
                ProjectionWork& work) {
    if (normalize(row)) {
        // At every supported t >= 0, parallel spatial normals retain exactly
        // the strongest rational intercept. This includes t = 0. Normalize
        // the direction separately; gcd of the complete homogeneous row alone
        // does not remove weaker parallel inequalities.
        Int direction_gcd = 0;
        for (std::size_t j = 1; j < row.size(); ++j) {
            direction_gcd = gcd(direction_gcd, absolute(row[j]));
        }
        Row key{};
        if (direction_gcd == 0) {
            if (row[0] >= 0) return;  // true at every nonnegative dilation
            row[0] = -1;             // retain impossibility for t > 0
        } else {
            for (std::size_t j = 1; j < row.size(); ++j) {
                key[j] = row[j] / direction_gcd;
            }
        }
        const auto old = rows.find(key);
        if (old == rows.end()) {
            rows.emplace(key, row);
        } else if (direction_gcd != 0) {
            Int old_gcd = 0;
            for (std::size_t j = 1; j < row.size(); ++j) {
                old_gcd = gcd(old_gcd, absolute(old->second[j]));
            }
            if (mul(row[0], old_gcd) < mul(old->second[0], direction_gcd)) {
                old->second = row;
            }
        }
        if (rows.size() > limits.projected_rows) {
            throw Failure("work_limit", "max-projected-rows exceeded");
        }
        work.peak_rows = std::max(work.peak_rows, rows.size());
    }
}

System eliminate(const System& rows, int coordinate, const Limits& limits,
                 ProjectionWork& work) {
    const int slot = coordinate + 1;
    std::vector<const Row*> positive;
    std::vector<const Row*> negative;
    std::map<Row, Row> result;
    for (const Row& row : rows) {
        if (row[slot] > 0) {
            positive.push_back(&row);
        } else if (row[slot] < 0) {
            negative.push_back(&row);
        } else {
            insert_row(result, row, limits, work);
        }
    }
    for (const Row* p : positive) {
        for (const Row* n : negative) {
            // Limits are at most 10^12, so this administrative increment
            // cannot wrap uint64_t before its explicit limit check.
            if (++work.pairs > limits.fm_pairs) {
                throw Failure("work_limit", "max-fm-pairs exceeded");
            }
            const Int positive_coefficient = (*p)[slot];
            const Int negative_magnitude = neg((*n)[slot]);
            const Int common = gcd(positive_coefficient, negative_magnitude);
            const Int p_multiplier = negative_magnitude / common;
            const Int n_multiplier = positive_coefficient / common;
            Row combined{};
            for (std::size_t j = 0; j < combined.size(); ++j) {
                // The eliminated entry is exactly zero by construction.
                // Avoid forming its two cancelling products unnecessarily.
                if (static_cast<int>(j) != slot) {
                    combined[j] = add(mul(p_multiplier, (*p)[j]),
                                      mul(n_multiplier, (*n)[j]));
                }
            }
            insert_row(result, combined, limits, work);
        }
    }
    // With only one sign, all inequalities involving this coordinate can be
    // satisfied by moving it sufficiently far in the appropriate direction.
    // Dropping them is exact existential real projection, never a box guess.
    System strongest;
    for (const auto& entry : result) strongest.push_back(entry.second);
    return strongest;
}

struct Projections {
    std::vector<System> prefix;       // prefix[k] involves only x_0,...,x_(k-1)
    std::vector<System> coordinate;   // full projection onto one coordinate
    ProjectionWork work;
};

Projections project(const Record& record, const Limits& limits) {
    Projections result;
    if (record.rows.size() > limits.projected_rows) {
        throw Failure("work_limit", "max-projected-rows exceeded by input system");
    }
    result.work.peak_rows = record.rows.size();
    result.prefix.resize(record.dimension + 1);
    result.prefix[record.dimension] = record.rows;
    for (int k = record.dimension - 1; k >= 0; --k) {
        result.prefix[k] = eliminate(result.prefix[k + 1], k, limits, result.work);
    }
    result.coordinate.resize(record.dimension);
    for (int target = 0; target < record.dimension; ++target) {
        if (target == 0) {
            result.coordinate[target] = result.prefix[1];
            continue;
        }
        System current = record.rows;
        for (int k = record.dimension - 1; k >= 0; --k) {
            if (k != target) {
                current = eliminate(current, k, limits, result.work);
            }
        }
        result.coordinate[target] = std::move(current);
    }
    return result;
}

struct Interval {
    bool have_lower = false;
    bool have_upper = false;
    bool impossible = false;
    Int lower = 0;
    Int upper = 0;
};

void constrain(Interval& interval, Int constant, Int coefficient) {
    if (coefficient > 0) {
        const Int lower = ceil_div(neg(constant), coefficient);
        if (!interval.have_lower || lower > interval.lower) {
            interval.lower = lower;
            interval.have_lower = true;
        }
    } else if (coefficient < 0) {
        const Int upper = floor_div(constant, neg(coefficient));
        if (!interval.have_upper || upper < interval.upper) {
            interval.upper = upper;
            interval.have_upper = true;
        }
    } else if (constant < 0) {
        interval.impossible = true;
    }
}

bool empty(const Interval& interval) {
    return interval.impossible || (interval.have_lower && interval.have_upper &&
                                    interval.lower > interval.upper);
}

struct CountWork {
    std::uint64_t search_nodes = 0;
    std::uint64_t final_intervals = 0;
};

class Enumerator {
public:
    Enumerator(const Record& record, const Projections& projections,
               const Limits& limits, std::int64_t dilation)
        : record_(record), projections_(projections), limits_(limits), t_(dilation) {}

    Int run() {
        // Eliminating every coordinate gives the exact real feasibility
        // conditions. Empty real polytopes contribute zero at this node.
        for (const Row& row : projections_.prefix[0]) {
            if (mul(row[0], t_) < 0) {
                return 0;
            }
        }
        if (record_.dimension == 0) {
            return 1;
        }
        bool integer_empty = false;
        for (int coordinate = 0; coordinate < record_.dimension; ++coordinate) {
            Interval bound;
            for (const Row& row : projections_.coordinate[coordinate]) {
                constrain(bound, mul(row[0], t_), row[coordinate + 1]);
            }
            if (!bound.have_lower || !bound.have_upper) {
                throw Failure("unbounded", "missing exact finite bound for coordinate " +
                                            std::to_string(coordinate));
            }
            integer_empty = integer_empty || empty(bound);
            global_[coordinate] = bound;
        }
        // Check every coordinate for unboundedness before returning zero for
        // an empty rounded interval in some other coordinate.
        return integer_empty ? 0 : branch(0);
    }

    CountWork work;

private:
    Int branch(int depth) {
        if (++work.search_nodes > limits_.search_nodes) {
            throw Failure("work_limit", "max-search-nodes exceeded for one record/dilation");
        }
        Interval interval = global_[depth];
        for (const Row& row : projections_.prefix[depth + 1]) {
            Int constant = mul(row[0], t_);
            for (int j = 0; j < depth; ++j) {
                constant = add(constant, mul(row[j + 1], values_[j]));
            }
            constrain(interval, constant, row[depth + 1]);
            if (empty(interval)) {
                return 0;
            }
        }
        if (!interval.have_lower || !interval.have_upper) {
            throw Failure("unresolved_bounds", "branch lacks proved finite bounds");
        }
        if (depth + 1 == record_.dimension) {
            // prefix[d] is the complete original normalized row system.
            // Its intersection in the final variable is precisely this
            // interval, so its integer cardinality is exact without a loop.
            ++work.final_intervals;
            return add(sub(interval.upper, interval.lower), 1);
        }
        Int result = 0;
        for (Int value = interval.lower;; value = add(value, 1)) {
            values_[depth] = value;
            result = add(result, branch(depth + 1));
            if (value == interval.upper) {
                break;
            }
        }
        return result;
    }

    const Record& record_;
    const Projections& projections_;
    const Limits& limits_;
    Int t_;
    std::array<Interval, 5> global_{};
    std::array<Int, 5> values_{};
};

class FreshOutput {
public:
    explicit FreshOutput(const std::string& path) {
        descriptor_ = ::open(path.c_str(), O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0600);
        if (descriptor_ < 0) {
            const int saved_errno = errno;
            throw Failure(saved_errno == EEXIST ? "output_exists" : "io",
                          "cannot exclusively create output: " + std::string(std::strerror(saved_errno)));
        }
    }
    ~FreshOutput() { if (descriptor_ >= 0) { ::close(descriptor_); } }
    FreshOutput(const FreshOutput&) = delete;
    FreshOutput& operator=(const FreshOutput&) = delete;

    void line(const std::string& value) {
        const std::string bytes = value + '\n';
        std::size_t position = 0;
        while (position < bytes.size()) {
            const auto written = ::write(descriptor_, bytes.data() + position, bytes.size() - position);
            if (written < 0 && errno == EINTR) {
                continue;
            }
            if (written <= 0) {
                throw Failure("io", "output write failed");
            }
            position += static_cast<std::size_t>(written);
        }
    }

    void finish() {
        if (::fsync(descriptor_) != 0) {
            throw Failure("io", "output fsync failed");
        }
        const int descriptor = descriptor_;
        descriptor_ = -1;
        if (::close(descriptor) != 0) {
            throw Failure("io", "output close failed");
        }
    }

private:
    int descriptor_ = -1;
};

struct CacheKey {
    int dimension;
    System complete_rows;
    bool operator<(const CacheKey& other) const {
        if (dimension != other.dimension) {
            return dimension < other.dimension;
        }
        return complete_rows < other.complete_rows;
    }
};

struct CacheEntry {
    std::size_t source_index;
    std::vector<Int> counts;
};

std::string output_record(const Record& record, std::size_t index,
                          const std::vector<std::int64_t>& nodes,
                          const std::vector<Int>& counts,
                          const std::vector<CountWork>& count_work,
                          const ProjectionWork& projection_work,
                          bool cache_hit, std::size_t cache_source) {
    std::string result = "{\"schema_version\":1,\"status\":\"complete\",\"id\":" + quote(record.id) +
        ",\"record_index\":" + std::to_string(index) +
        ",\"dimension\":" + std::to_string(record.dimension) +
        ",\"input_rows\":" + std::to_string(record.input_rows) +
        ",\"normalized_rows\":" + std::to_string(record.rows.size()) +
        ",\"native_calls\":0,\"nodes\":[";
    for (std::size_t j = 0; j < nodes.size(); ++j) {
        result += (j == 0 ? "" : ",") + std::to_string(nodes[j]);
    }
    result += "],\"counts\":[";
    for (std::size_t j = 0; j < counts.size(); ++j) {
        result += (j == 0 ? "" : ",") + quote(decimal(counts[j]));
    }
    result += "],\"cache_hit\":" + std::string(cache_hit ? "true" : "false") +
              ",\"cache_source_record_index\":" + std::to_string(cache_source) +
              ",\"fm_pairs\":" + std::to_string(projection_work.pairs) +
              ",\"peak_projected_rows\":" + std::to_string(projection_work.peak_rows) +
              ",\"search_nodes\":[";
    for (std::size_t j = 0; j < count_work.size(); ++j) {
        result += (j == 0 ? "" : ",") + std::to_string(count_work[j].search_nodes);
    }
    result += "],\"final_intervals\":[";
    for (std::size_t j = 0; j < count_work.size(); ++j) {
        result += (j == 0 ? "" : ",") + std::to_string(count_work[j].final_intervals);
    }
    return result + "]}";
}
}  // namespace

int main(int argc, char** argv) {
    std::int64_t active_record = -1;
    std::string active_id;
    try {
        if (argc == 2 && std::string(argv[1]) == "--help") {
            std::cout << "Usage: chart_counter_v1 --input FILE --start INCLUSIVE --stop EXCLUSIVE "
                         "--nodes T0,T1,... --output FRESH_FILE [--no-cache] "
                         "[--max-fm-pairs N] [--max-projected-rows N] [--max-search-nodes N]\n";
            return 0;
        }
        const Options options = parse_options(argc, argv);
        const auto records = read_records(options.input);
        if (options.stop > records.size()) {
            throw Failure("input_domain", "stop exceeds declared record count");
        }
        FreshOutput output(options.output);
        std::map<CacheKey, CacheEntry> cache;
        std::size_t cached_rows = 0;
        std::size_t cache_hits = 0;
        for (std::size_t index = options.start; index < options.stop; ++index) {
            active_record = static_cast<std::int64_t>(index);
            const Record& record = records[index];
            active_id = record.id;
            CacheKey key{record.dimension, record.rows};
            const auto cached = options.cache ? cache.find(key) : cache.end();
            const bool hit = cached != cache.end();
            std::vector<Int> counts;
            std::vector<CountWork> count_work(options.nodes.size());
            ProjectionWork projection_work;
            std::size_t cache_source = index;
            if (hit) {
                counts = cached->second.counts;
                cache_source = cached->second.source_index;
                ++cache_hits;
            } else {
                const Projections projections = project(record, options.limits);
                projection_work = projections.work;
                for (std::size_t j = 0; j < options.nodes.size(); ++j) {
                    Enumerator enumerator(record, projections, options.limits, options.nodes[j]);
                    counts.push_back(enumerator.run());
                    count_work[j] = enumerator.work;
                }
                // Equality compares the entire normalized complete row set
                // and dimension. There is no hash/signature-only acceptance.
                // All entries in this process share the same frozen node list.
                if (options.cache && cache.size() < 4096 && cached_rows + key.complete_rows.size() <= 100000) {
                    cached_rows += key.complete_rows.size();
                    cache.emplace(std::move(key), CacheEntry{index, counts});
                }
            }
            output.line(output_record(record, index, options.nodes, counts, count_work,
                                      projection_work, hit, cache_source));
        }
        output.finish();
        std::cout << "{\"status\":\"complete\",\"records\":" << options.stop - options.start
                  << ",\"cache_hits\":" << cache_hits << ",\"native_calls\":0}\n";
        return 0;
    } catch (const Failure& error) {
        std::cerr << "{\"status\":\"failed\",\"error_type\":" << quote(error.type)
                  << ",\"message\":" << quote(error.what())
                  << ",\"record_index\":" << active_record << ",\"id\":" << quote(active_id) << "}\n";
        return 1;
    } catch (const std::exception& error) {
        std::cerr << "{\"status\":\"failed\",\"error_type\":\"internal\",\"message\":"
                  << quote(error.what()) << ",\"record_index\":" << active_record << "}\n";
        return 1;
    }
}
