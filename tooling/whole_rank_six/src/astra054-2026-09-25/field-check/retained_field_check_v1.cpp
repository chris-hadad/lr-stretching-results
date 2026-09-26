// A54: exact, source-bound check of an A19 field on a retained row mask.
// The only scientific implementation dependency is the accepted A19 common header.
#include "../../astra019-2026-09-18/field/common_v1.hpp"

namespace {
constexpr const char* DENOMINATOR = "10000000000"; // A19 D; beta = alpha + B*n/(6D)
const Q EPSILON = Q(1, 2000000); // Adopted candidate bound; not a promoted theorem.

__int128 add128(__int128 a, __int128 b) {
    __int128 c;
    need(!__builtin_add_overflow(a, b, &c), "int128 addition overflow");
    return c;
}

__int128 mul128(__int128 a, __int128 b) {
    __int128 c;
    need(!__builtin_mul_overflow(a, b, &c), "int128 multiplication overflow");
    return c;
}

struct MappedMatrix {
    std::string scope;
    uint32_t begin, end, coords;
    uint64_t nnz;
    Map columns, values, degrees, norms;

    explicit MappedMatrix(const fs::path& p)
        : columns(p / "columns.u32"), values(p / "coefficients.i8"),
          degrees(p / "degrees.u8"), norms(p / "norms.u16") {
        std::ifstream f(p / "HEADER.txt");
        std::string magic, a, b, c, d, tail;
        need(bool(f >> magic >> scope >> a >> b >> c >> d) &&
                 magic == "A19_MATRIX_V1" && !(f >> tail), "A19 matrix header");
        begin = u32arg(a); end = u32arg(b); coords = u32arg(c); nnz = number(d);
        need(begin < end && end <= FIELD_ROWS && coords > 0 &&
                 coords <= FIELD_COORDS && nnz > 0 && nnz <= FIELD_NNZ &&
                 (scope == "original" || scope == "synthetic"), "A19 matrix dimensions");
        need(scope != "original" || coords == FIELD_COORDS,
             "original global coordinate dimension");
        need(columns.n == 4 * nnz && values.n == nnz &&
                 degrees.n == end - begin && norms.n == 2ull * (end - begin),
             "complete matrix arrays");
    }
    uint32_t rows() const { return end - begin; }
};

struct RHSList {
    std::vector<fs::path> paths;
    RHSList(const fs::path& list, const MappedMatrix& m) {
        std::ifstream f(list); need(bool(f), "open RHS list");
        std::string line; uint32_t next = m.begin;
        while (std::getline(f, line)) {
            need(!line.empty(), "nonempty RHS list line");
            fs::path p(line);
            RHS rhs(p);
            need(rhs.scope == m.scope && rhs.begin == next && rhs.end <= m.end,
                 "consecutive exact RHS coverage and scope");
            paths.push_back(p); next = rhs.end;
        }
        need(f.eof() && !paths.empty() && next == m.end,
             "complete exact RHS coverage");
    }
};

uint32_t optional_support(Cache& cache, uint32_t ordinal) {
    uint32_t lo = 0, hi = SUPPORTS;
    while (lo < hi) {
        uint32_t mid = lo + (hi - lo) / 2;
        if (le(cache.lookup.p + 8ull * mid, 4) < ordinal) lo = mid + 1;
        else hi = mid;
    }
    return lo < SUPPORTS && le(cache.lookup.p + 8ull * lo, 4) == ordinal
               ? le(cache.lookup.p + 8ull * lo + 4, 4) : UINT32_MAX;
}

struct Minimum {
    bool seen = false;
    Q value;
    uint64_t ties = 0;
    std::vector<uint32_t> sample;
    void add(const Q& q, uint32_t row) {
        if (!seen || q < value) {
            seen = true; value = q; ties = 1; sample = {row};
        } else if (q == value) {
            ++ties;
            if (sample.size() < 16) sample.push_back(row);
        }
    }
};

void json_min(std::ostream& out, const char* name, const Minimum& m) {
    out << '\"' << name << "\":{\"value\":";
    if (m.seen) out << '\"' << m.value.get_str() << '\"'; else out << "null";
    out << ",\"ties\":" << m.ties << ",\"sample_rows\":[";
    for (size_t i = 0; i < m.sample.size(); ++i) {
        if (i) out << ',';
        out << m.sample[i];
    }
    out << "]}";
}

int check(const fs::path& atlas, const fs::path& parents,
          const fs::path& cachepath, const fs::path& matrix,
          const fs::path& rhs_list, const fs::path& numerators,
          const fs::path& classes, const Z& D, const fs::path& output) {
    auto started = std::chrono::steady_clock::now();
    need(D == Z(DENOMINATOR), "Fable field requires A19 D=10000000000");
    freshpath(output);
    MappedMatrix m(matrix);
    RHSList rhs_paths(rhs_list, m);
    Map field(numerators), mask(classes);
    need(field.n == 8ull * m.coords, "exact i64 field length");
    need(mask.n == m.rows(), "exact class mask length");
    std::unique_ptr<Map> source;
    std::unique_ptr<Cache> cache;
    std::vector<uint8_t> verified;
    if (m.scope == "original") {
        init(atlas);
        for (auto& r : N) for (int n : r)
            need(std::abs(n) <= 4, "A19 original normal bound");
        source.reset(new Map(parents));
        cache.reset(new Cache(cachepath));
        need(source->n == 8ull * FIELD_ROWS, "complete original q9 roster");
        verified.resize(SUPPORTS, 0);
    }
    auto numerator = [&](uint32_t col) -> I {
        need(col < m.coords, "actual field coordinate");
        uint64_t raw = le(field.p + 8ull * col, 8);
        I value; std::memcpy(&value, &raw, 8); return value;
    };
    uint64_t counts[3]{}, selected_below_epsilon = 0;
    uint64_t selected_nonpositive = 0, selected_negative = 0;
    uint64_t class0_negative = 0, selected_orbit_multiplicity = 0;
    uint64_t primitive_incidences = 0, verified_supports = 0, offset = 0;
    Minimum selected_min, all_min, class0_min;
    uint32_t row = m.begin;
    for (const auto& path : rhs_paths.paths) {
        RHS rhs(path);
        for (; row < rhs.end; ++row) {
            uint32_t local = row - m.begin;
            uint8_t cls = mask.p[local];
            need(cls <= 2, "class mask value must be 0, 1 or 2");
            ++counts[cls];
            uint8_t degree = m.degrees.p[local];
            need(degree <= 18 && (m.scope != "original" || degree >= 2),
                 "A19 row degree bound");
            __int128 stored = 0;
            I norm = 0; uint32_t previous = 0;
            for (unsigned j = 0; j < degree; ++j) {
                need(offset < m.nnz, "matrix entry count");
                uint32_t col = le(m.columns.p + 4ull * offset, 4);
                I coefficient = int8_t(m.values.p[offset]);
                need(col < m.coords && (j == 0 || col > previous) &&
                         coefficient && coefficient >= -38 && coefficient <= 38,
                     "sorted unique bounded matrix entry");
                previous = col;
                norm += coefficient * coefficient;
                stored = add128(stored, mul128(coefficient, numerator(col)));
                ++offset;
            }
            need(norm == I(le(m.norms.p + 2ull * local, 2)) && norm <= 25992,
                 "exact stored matrix norm");
            uint32_t ordinal = row, index = 1;
            if (source) {
                auto p = source->p + 8ull * row;
                ordinal = le(p, 4); index = le(p + 4, 2);
                need(index > 0 && p[7] <= 1, "q9 record index and membership width");
                if (row > 0)
                    need(le(source->p + 8ull * (row - 1), 4) < ordinal,
                         "strict original q9 ordinal order");
            }
            if (source && cls > 0) {
                auto p = source->p + 8ull * row;
                Row parent = unrank(ordinal, 9);
                auto orbit = canonical(parent, 9);
                auto image = imageof(parent, 9);
                need(orbit.ordinal == ordinal && orbit.stabilizer == p[6] &&
                         image.index == index && image.ones == bool(p[7]),
                     "original q9 orbit, image index and membership");
                selected_orbit_multiplicity += 6 / orbit.stabilizer;
                __int128 direct = 0;
                for (int g = 0; g < 6; ++g) {
                    Row transformed{};
                    for (int j = 0; j < 9; ++j) transformed[j] = G[g][parent[j]];
                    std::sort(transformed.begin(), transformed.end());
                    for (int deleted = 0; deleted < 9; ++deleted) {
                        Row face{}; int j = 0;
                        for (int i = 0; i < 9; ++i)
                            if (i != deleted) face[j++] = transformed[i];
                        uint32_t support = optional_support(*cache, rankof(face, 8));
                        if (support == UINT32_MAX) continue;
                        auto k = cache->get(support);
                        I support_index = le(k + 80, 2);
                        if (!verified[support]) {
                            need(imageof(face, 8).index == support_index,
                                 "independent support image index");
                            for (int i = 0; i < 8; ++i) for (int a = 0; a < 2; ++a) {
                                I z = 0;
                                for (int c = 0; c < 10; ++c)
                                    z += I(N[face[i]][c]) * small(k + 2 * (2 * c + a));
                                need(z == 0, "independent kernel annihilation");
                            }
                            for (int a = 0; a < 2; ++a) for (int b = 0; b < 2; ++b) {
                                I z = 0;
                                for (int c = 0; c < 10; ++c)
                                    z += I(small(k + 40 + 2 * (10 * a + c))) *
                                         small(k + 2 * (2 * c + b));
                                need(z == (a == b), "independent saturated left inverse");
                            }
                            verified[support] = 1; ++verified_supports;
                        }
                        I height[2]{}; __int128 ambient[10]{};
                        for (int c = 0; c < 10; ++c) for (int a = 0; a < 2; ++a) {
                            I basis = small(k + 2 * (2 * c + a));
                            height[a] += I(N[transformed[deleted]][c]) * basis;
                            ambient[c] = add128(ambient[c],
                                                mul128(basis, numerator(2 * support + a)));
                        }
                        I divisor = std::gcd(std::abs(height[0]), std::abs(height[1]));
                        need(divisor > 0 && I(index) == divisor * support_index,
                             "independent primitive quotient index");
                        __int128 contraction = 0;
                        for (int c = 0; c < 10; ++c)
                            contraction = add128(contraction,
                                mul128(N[transformed[deleted]][c], ambient[c]));
                        need(contraction % divisor == 0,
                             "exact original primitive contraction");
                        direct = add128(direct, contraction / divisor);
                        ++primitive_incidences;
                    }
                }
                need(stored == direct,
                     "stored sparse matrix versus independent original action");
            }
            Q alpha = rhs.get(row, ordinal, index);
            Q beta = alpha + Q(big(stored), Z(6) * D);
            beta.canonicalize();
            all_min.add(beta, row);
            if (cls == 0) {
                class0_min.add(beta, row);
                class0_negative += beta < 0;
            } else {
                selected_min.add(beta, row);
                selected_below_epsilon += beta < EPSILON;
                selected_nonpositive += beta <= 0;
                selected_negative += beta < 0;
            }
        }
    }
    need(row == m.end && offset == m.nnz, "complete matrix and RHS traversal");
    need(counts[0] + counts[1] + counts[2] == m.rows(), "complete class partition");
    rusage usage{}; getrusage(RUSAGE_SELF, &usage);
    std::ofstream out(output); need(bool(out), "open fresh exact result");
    std::string status = !selected_min.seen ? "EMPTY_SELECTION" :
                         selected_below_epsilon ? "FAIL_RETAINED_BELOW_EPSILON" :
                         "PASS_RETAINED_AT_LEAST_EPSILON";
    out << "{\"schema\":\"astra054-retained-field-check/v1\",\"status\":\""
        << status << "\",\"scope\":\"" << m.scope << "\",\"begin\":"
        << m.begin << ",\"end\":" << m.end << ",\"rows\":" << m.rows()
        << ",\"nnz\":" << m.nnz << ",\"coordinates\":" << m.coords
        << ",\"D\":\"" << D << "\",\"actual_denominator\":\""
        << Z(6) * D << "\",\"epsilon\":\"" << EPSILON
        << "\",\"class_counts\":[" << counts[0] << ','
        << counts[1] << ',' << counts[2] << "],\"retained_rows\":"
        << counts[1] + counts[2] << ",\"retained_below_epsilon\":"
        << selected_below_epsilon << ",\"retained_nonpositive\":"
        << selected_nonpositive << ",\"retained_negative\":"
        << selected_negative << ",\"class0_negative_control_count\":"
        << class0_negative << ",\"selected_original_multiplicity\":"
        << selected_orbit_multiplicity << ",\"primitive_incidences\":"
        << primitive_incidences << ",\"support_blocks_independently_checked\":"
        << verified_supports << ',';
    json_min(out, "retained_minimum", selected_min); out << ',';
    json_min(out, "full_domain_minimum", all_min); out << ',';
    json_min(out, "class0_minimum", class0_min);
    out << ",\"seconds\":" << std::setprecision(17)
        << std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count()
        << ",\"peak_rss_bytes\":" << usage.ru_maxrss << "}\n";
    out.close(); need(bool(out), "complete exact result output");
    return status == "PASS_RETAINED_AT_LEAST_EPSILON" ? 0 : 4;
}
} // namespace

int main(int argc, char** argv) {
    try {
        uint16_t endian = 1;
        need(*(unsigned char*)&endian == 1 && sizeof(long) == 8,
             "declared little-endian 64-bit host");
        need(argc == 10,
             "usage: checker atlas parents cache matrix rhs-list numerators classes D result");
        return check(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6],
                     argv[7], positiveZ(argv[8]), argv[9]);
    } catch (const std::exception& e) {
        std::cerr << "REFUSED: " << e.what() << '\n';
        return 2;
    }
}
