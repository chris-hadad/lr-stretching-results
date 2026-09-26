// Complete atlas-derived fields, all mixed terms, and all balancing directions.
#include "common.hpp"
using namespace lf;

struct Assignment {
    std::array<int, 3> masks{};
    std::array<std::vector<std::pair<int, I>>, 7> terms;
};
struct Templates {
    I inverse[7][3][3]{};
    std::vector<Assignment> assignments;
    I maximum = 0;
};
Templates read_templates(const std::string& path) {
    std::ifstream in(path);
    require(bool(in), "Missing independent templates");
    std::string magic;
    in >> magic;
    require(magic == "LFTEMPLATES1", "Wrong template schema");
    require(integer(in, "assignments") == 1024 && integer(in, "chambers") == 7
            && integer(in, "positions") == 165 && integer(in, "denominator") == DEN, "Wrong complete template dimensions");
    Templates t;
    const I rays[7][3][3] = {
        {{1,0,0},{0,0,1},{1,1,1}}, {{0,0,1},{0,1,1},{1,1,1}},
        {{1,0,0},{1,1,0},{1,1,1}}, {{1,1,0},{0,1,0},{1,2,1}},
        {{0,1,1},{0,1,0},{1,2,1}}, {{1,1,0},{1,1,1},{1,2,1}},
        {{0,1,1},{1,1,1},{1,2,1}}
    };
    for (int c = 0; c < 7; ++c) {
        for (auto& row : t.inverse[c]) for (I& value : row) {
            value = integer(in, "inverse coordinate");
            require(value >= -4 && value <= 4, "Inverse entry out of range");
        }
        for (int i = 0; i < 3; ++i) for (int j = 0; j < 3; ++j) {
            I left = 0, right = 0;
            for (int k = 0; k < 3; ++k) {
                left += t.inverse[c][i][k] * rays[c][j][k];
                right += rays[c][k][i] * t.inverse[c][k][j];
            }
            require(left == (i == j) && right == (i == j), "A3 inverse identity failed");
        }
    }
    t.assignments.resize(1024);
    for (int id = 0; id < 1024; ++id) {
        require(integer(in, "assignment identity") == id, "Missing or duplicate assignment");
        auto& a = t.assignments[id];
        std::array<int, 3> actual{};
        int number = id;
        for (int column = 4; column >= 0; --column, number /= 4) {
            int label = number % 4;
            for (int i = 0; i < 3; ++i) if (label <= i) actual[i] |= 1 << column;
        }
        for (int i = 0; i < 3; ++i) {
            a.masks[i] = int(integer(in, "assignment mask"));
            require(a.masks[i] == actual[i], "Assignment masks disagree with all labeled assignments");
        }
        for (int c = 0; c < 7; ++c) for (int k = 0; k < 165; ++k) {
            I value = integer(in, "template entry");
            require(value >= -TBOUND && value <= TBOUND, "Template overflow bound exceeded");
            t.maximum = std::max(t.maximum, std::abs(value));
            if (value) a.terms[c].push_back({k, value});
        }
    }
    eof(in, "templates");
    return t;
}

int select_chamber(const Templates& t, I x, I y, I z) {
    if (x < 0 || y < 0 || z < 0) return -1;
    std::array<I, 3> slope{x, y, z};
    int selected = -1;
    for (int c = 0; c < 7; ++c) {
        bool inside = true;
        for (const auto& row : t.inverse[c]) {
            I value = 0;
            for (int j = 0; j < 3; ++j) value += row[j] * slope[j];
            if (value <= 0) { inside = false; break; }
        }
        if (inside) {
            require(selected == -1, "Nonunique supported A3 chamber");
            selected = c;
        }
    }
    require(selected != -1, "Generic positive A3 slope has no strict chamber");
    return selected;
}

struct BinaryFields {
    std::ifstream input;
    I first, last, width;
    BinaryFields(const std::string& path, I positions, I lo, I hi) : input(path, std::ios::binary) {
        require(bool(input), "Missing field comparison input");
        first = get_i64(input); last = get_i64(input); width = get_i64(input);
        require(get_i64(input) == DEN && width == positions, "Wrong field header");
        require(first >= 0 && first <= lo && lo < hi && hi <= last && last <= 591214,
                "Field comparison interval differs");
        require(std::filesystem::file_size(path) == uint64_t(32 + (last - first) * (width + 1) * 8),
                "Truncated or trailing binary field data");
        input.seekg(32 + (lo - first) * (width + 1) * 8);
        require(bool(input), "Cannot seek to field interval");
    }
    std::vector<I> next(I id) {
        require(get_i64(input) == id, "Missing, duplicate, or wrong field identity");
        std::vector<I> out;
        for (I j = 0; j < width; ++j) {
            I value = get_i64(input);
            require(value >= -FBOUND && value <= FBOUND, "Source field overflow bound exceeded");
            out.push_back(value);
        }
        return out;
    }
};

struct Minimum {
    bool initialized = false;
    W value = 0;
    void observe(W x) { if (!initialized || x < value) value = x; initialized = true; }
};
struct RayValue { bool set = false; W q2 = 0, q3 = 0; I occurrences = 0; };
I derive_tensors(const std::array<I, 165>& field, I (&B)[8][8], I (&S)[8][8][8]) {
    int slot = 9;
    I maximum = 0;
    for (int a = 0; a < 8; ++a) for (int b = a; b < 8; ++b) {
        I value = field[slot++];
        require(value >= -FBOUND && value <= FBOUND, "Quadratic tensor input bound exceeded");
        B[a][b] += value; B[b][a] += value;
        maximum = std::max(maximum, std::abs(value));
    }
    for (int a = 0; a < 8; ++a) for (int b = a; b < 8; ++b) for (int c = b; c < 8; ++c) {
        I value = field[slot++];
        require(value >= -FBOUND && value <= FBOUND, "Cubic tensor input bound exceeded");
        maximum = std::max(maximum, std::abs(value));
        std::array<int, 3> labels{a, b, c}, positions{0, 1, 2};
        // Differentiate by all ordered label positions, retaining multiplicity.
        do { S[labels[positions[0]]][labels[positions[1]]][labels[positions[2]]] += value; }
        while (std::next_permutation(positions.begin(), positions.end()));
    }
    require(slot == 165, "Low-field monomial roster incomplete");
    return maximum;
}
void positive(W value, const std::string& label, I cell, int a, int b = -1, int c = -1) {
    if (value < 0) {
        throw std::runtime_error("ADVERSE " + label + " cell=" + std::to_string(cell)
              + " indices=" + std::to_string(a) + "," + std::to_string(b) + "," + std::to_string(c)
              + " exact_numerator=" + decimal(value));
    }
}
void write_field(std::ostream& out, I identity, const std::array<I, 165>& field) {
    std::array<unsigned char, 166 * 8> raw;
    for (size_t i = 0; i < 166; ++i) {
        uint64_t value = uint64_t(i ? field[i - 1] : identity);
        for (int b = 0; b < 8; ++b) raw[i * 8 + b] = (value >> (8 * b)) & 255;
    }
    out.write(reinterpret_cast<const char*>(raw.data()), raw.size());
    require(bool(out), "Independent field write failed");
}

void self_test(const std::string& output) {
    // The squared difference has nonnegative pure coordinate values and a
    // negative mixed pair. The cubed difference tests repeated multiplicities,
    // a negative mixed triple, and a negative balancing derivative.
    std::array<I, 165> field{};
    int slot = 9;
    for (int a = 0; a < 8; ++a) for (int b = a; b < 8; ++b) {
        field[slot++] = a == 0 && b == 0 ? 1 : a == 0 && b == 1 ? -2 : a == 1 && b == 1 ? 1 : 0;
    }
    for (int a = 0; a < 8; ++a) for (int b = a; b < 8; ++b) for (int c = b; c < 8; ++c) {
        I value = 0;
        if (c <= 1) { int ones = (a == 1) + (b == 1) + (c == 1); value = ones == 0 ? 1 : ones == 1 ? -3 : ones == 2 ? 3 : -1; }
        field[slot++] = value;
    }
    I B[8][8]{}, S[8][8][8]{};
    derive_tensors(field, B, S);
    require(B[0][0] == 2 && B[1][1] == 2 && B[0][1] == -2, "Quadratic mixed-term negative control failed");
    require(S[0][0][0] == 6 && S[0][0][1] == -6 && S[0][1][1] == 6 && S[1][1][1] == -6,
            "Cubic repeated-index multiplicity control failed");
    Ray x{2, 1, 0, 0, 0, 0, 0, 0}, b{-1, 1, 0, 0, 0, 0, 0, 0};
    W q = 0, c = 0, dq = 0, dc = 0;
    for (int i = 0; i < 8; ++i) for (int j = 0; j < 8; ++j) {
        q += W(B[i][j]) * x[i] * x[j]; dq += W(B[i][j]) * b[i] * x[j];
        for (int k = 0; k < 8; ++k) { c += W(S[i][j][k]) * x[i] * x[j] * x[k]; dc += W(S[i][j][k]) * b[i] * x[j] * x[k]; }
    }
    require(q == 2 && c == 6 && dq == -4 && dc == -12, "Polynomial and derivative identity control failed");
    int refusals = 0;
    for (W negative : {W(B[0][1]), W(S[0][0][1]), dq, dc}) {
        try { positive(negative, "intentional synthetic negative", -1, 0); }
        catch (const std::runtime_error&) { ++refusals; }
    }
    require(refusals == 4, "A negative mixed criterion was accepted");
    bool overflow_refused = false;
    try { narrow(W(std::numeric_limits<I>::max()) + 1, "intentional overflow"); }
    catch (const std::runtime_error&) { overflow_refused = true; }
    require(overflow_refused && cuts().size() == 210 && balancing().size() == 16, "Overflow or complete roster control failed");
    auto report = fresh(std::filesystem::path(output) / "FIELD-CONTROLS.json");
    report << "{\"status\":\"PASS\",\"polynomial_identities\":4,\"negative_criterion_refusals\":4,\"overflow_refusals\":1,\"proper_cuts\":210,\"balancing_directions\":16}\n";
}

int main(int argc, char** argv) {
    std::string out;
    I current = -1;
    try {
        if (argc == 3 && std::string(argv[1]) == "--self-test") { out = argv[2]; self_test(out); return 0; }
        require(argc == 9, "Expected state templates quadratic-bin cubic-bin part lo hi output");
        out = argv[8];
        require(std::filesystem::is_directory(out), "Runner output directory is missing");
        std::string part_string = argv[5];
        require(part_string.size() == 1, "Malformed domain part");
        char part = part_string[0];
        I lo = argument_integer(argv[6]), hi = argument_integer(argv[7]);
        auto started = std::chrono::steady_clock::now();
        State state = read_state(argv[1], part, lo, hi);
        Templates templates = read_templates(argv[2]);
        BinaryFields quadratic(argv[3], 45, lo, hi), cubic(argv[4], 120, lo, hi);
        auto primary = fresh(std::filesystem::path(out) / "fields.bin", true);
        for (I value : {lo, hi, I(165), DEN}) put_i64(primary, value);
        std::vector<int> previous(1024, -1);
        std::array<I, 165> field{};
        std::vector<RayValue> restrictions(state.vertices.size());
        auto directions = balancing();
        I pairs = 0, triples = 0, ray_occurrences = 0, changed_assignments = 0, supported = 0;
        I maximum_field = 0;
        Minimum q2_min, q3_min, q2_columns, q2_rows, q3_columns, q3_rows;
        for (I id = lo; id < hi; ++id) {
            current = id;
            const auto& cell = state.cells[size_t(id - lo)];
            cell_signature(state, cell);
            Ray center{};
            I largest_coordinate = 0;
            for (int vertex : cell) for (int j = 0; j < 8; ++j) {
                center[j] += state.vertices[vertex][j];
                largest_coordinate = std::max(largest_coordinate, state.vertices[vertex][j]);
            }
            // A positive sum of all homogeneous rays is an interior selector.
            std::array<I, 5> columns{center[3], center[4], center[5], center[6], center[7] - center[3] - center[4] - center[5] - center[6]};
            std::array<I, 32> subset{};
            for (int mask = 1; mask < 32; ++mask) {
                int bit = __builtin_ctz(unsigned(mask));
                subset[mask] = subset[mask & (mask - 1)] + columns[bit];
            }
            for (int assignment = 0; assignment < 1024; ++assignment) {
                const auto& a = templates.assignments[assignment];
                int chamber = select_chamber(templates, subset[a.masks[0]] - center[0],
                        subset[a.masks[1]] - center[0] - center[1],
                        subset[a.masks[2]] - center[0] - center[1] - center[2]);
                supported += chamber >= 0;
                if (previous[assignment] == chamber) continue;
                ++changed_assignments;
                // Induction preserves the complete 1024-assignment sum. Each
                // intermediate is bounded by 2 * 1024 * TBOUND < INT64_MAX.
                if (previous[assignment] >= 0) for (auto [k, value] : a.terms[previous[assignment]]) field[k] -= value;
                if (chamber >= 0) for (auto [k, value] : a.terms[chamber]) field[k] += value;
                previous[assignment] = chamber;
            }
            for (I value : field) {
                require(value >= -FBOUND && value <= FBOUND, "Whole field accumulation escaped its proven bound");
                maximum_field = std::max(maximum_field, std::abs(value));
            }
            write_field(primary, id, field);
            auto q2_source = quadratic.next(id), q3_source = cubic.next(id);
            for (int j = 0; j < 45; ++j) if (field[j] != q2_source[j]) {
                primary.flush();
                throw std::runtime_error("Complete low-field identity mismatch at cell=" + std::to_string(id) + " slot=" + std::to_string(j));
            }
            for (int j = 0; j < 120; ++j) if (field[45 + j] != q3_source[j]) {
                primary.flush();
                throw std::runtime_error("Cubic field identity mismatch at cell=" + std::to_string(id) + " slot=" + std::to_string(j));
            }
            require(field[0] == DEN, "Derived whole constant coefficient is not one");
            I B[8][8]{}, S[8][8][8]{};
            I max_coefficient = derive_tensors(field, B, S);
            require(W(6) * max_coefficient * 64 * largest_coordinate * largest_coordinate <= std::numeric_limits<I>::max(),
                    "Intermediate contraction exceeds the declared int64 engineering bound");
            // Final dot products use signed 128 bits. Input bounds imply the
            // absolute full contraction is <= 512*6*FBOUND*VBOUND^3 < 2^127.
            size_t n = cell.size();
            std::vector<std::array<I, 8>> Bv(n);
            std::vector<std::array<I, 64>> Sv(n);
            for (size_t i = 0; i < n; ++i) {
                const Ray& v = state.vertices[cell[i]];
                for (int a = 0; a < 8; ++a) {
                    W value = 0;
                    for (int b = 0; b < 8; ++b) value += W(B[a][b]) * v[b];
                    Bv[i][a] = narrow(value, "quadratic first contraction");
                    for (int b = 0; b < 8; ++b) {
                        W third = 0;
                        for (int c = 0; c < 8; ++c) third += W(S[a][b][c]) * v[c];
                        Sv[i][a * 8 + b] = narrow(third, "cubic first contraction");
                    }
                }
                for (int d = 0; d < 16; ++d) {
                    W value = 0;
                    for (int k = 0; k < 8; ++k) value += W(Bv[i][k]) * directions[d][k];
                    positive(value, "c2 balancing", id, int(i), d);
                    (d < 10 ? q2_columns : q2_rows).observe(value);
                }
                ++ray_occurrences;
            }
            for (size_t i = 0; i < n; ++i) for (size_t j = i; j < n; ++j) {
                const Ray& vj = state.vertices[cell[j]];
                W q2 = 0;
                std::array<I, 8> pair{};
                for (int a = 0; a < 8; ++a) {
                    q2 += W(Bv[i][a]) * vj[a];
                    W value = 0;
                    for (int b = 0; b < 8; ++b) value += W(Sv[i][a * 8 + b]) * vj[b];
                    pair[a] = narrow(value, "cubic second contraction");
                }
                positive(q2, "c2 mixed pair", id, int(i), int(j));
                q2_min.observe(q2); ++pairs;
                for (int d = 0; d < 16; ++d) {
                    W value = 0;
                    for (int a = 0; a < 8; ++a) value += W(pair[a]) * directions[d][a];
                    positive(value, "c3 balancing", id, int(i), int(j), d);
                    (d < 10 ? q3_columns : q3_rows).observe(value);
                }
                for (size_t k = j; k < n; ++k) {
                    const Ray& vk = state.vertices[cell[k]];
                    W value = 0;
                    for (int a = 0; a < 8; ++a) value += W(pair[a]) * vk[a];
                    positive(value, "c3 mixed triple", id, int(i), int(j), int(k));
                    q3_min.observe(value); ++triples;
                    if (i == j && j == k) {
                        require(q2 % 2 == 0 && value % 6 == 0, "Pure derivative multiplicity is not exact");
                        auto& r = restrictions[cell[i]];
                        if (r.set) require(r.q2 == q2 / 2 && r.q3 == value / 6, "Repeated ray restrictions disagree");
                        else { r.set = true; r.q2 = q2 / 2; r.q3 = value / 6; }
                        ++r.occurrences;
                    }
                }
            }
        }
        primary.flush(); require(bool(primary), "Independent field output failed");
        auto rays = fresh(std::filesystem::path(out) / "rays.txt");
        I distinct = 0, q2_zeros = 0, q3_zeros = 0;
        for (size_t v = 0; v < restrictions.size(); ++v) if (restrictions[v].set) {
            const auto& r = restrictions[v];
            rays << v;
            for (I value : state.vertices[v]) rays << ' ' << value;
            rays << ' ' << actual_dimension(state.vertices[v]) << ' ' << decimal(r.q2) << ' ' << decimal(r.q3) << ' ' << r.occurrences << '\n';
            ++distinct; q2_zeros += r.q2 == 0; q3_zeros += r.q3 == 0;
        }
        rays.flush(); require(bool(rays), "Ray restriction output failed");
        auto report = fresh(std::filesystem::path(out) / "FIELD-BATCH.json");
        report << "{\"schema\":\"pro030-independent-field-batch/v1\",\"status\":\"PASS\",\"part\":\"" << part
               << "\",\"lo\":" << lo << ",\"hi\":" << hi << ",\"cells\":" << hi - lo
               << ",\"positions\":" << (hi - lo) * 165 << ",\"assignment_visits\":" << (hi - lo) * 1024
               << ",\"supported_assignments\":" << supported << ",\"changed_assignments\":" << changed_assignments
               << ",\"maximum_absolute_field_entry\":" << maximum_field << ",\"pairs\":" << pairs << ",\"triples\":" << triples
               << ",\"ray_occurrences\":" << ray_occurrences << ",\"c2_column_checks\":" << ray_occurrences * 10
               << ",\"c2_row_checks\":" << ray_occurrences * 6 << ",\"c3_column_checks\":" << pairs * 10
               << ",\"c3_row_checks\":" << pairs * 6 << ",\"distinct_rays_in_batch\":" << distinct
               << ",\"quadratic_zero_rays_in_batch\":" << q2_zeros << ",\"cubic_zero_rays_in_batch\":" << q3_zeros
               << ",\"minimum_q2_pair\":\"" << decimal(q2_min.value) << "\",\"minimum_q3_triple\":\"" << decimal(q3_min.value)
               << "\",\"minimum_q2_column\":\"" << decimal(q2_columns.value) << "\",\"minimum_q2_row\":\"" << decimal(q2_rows.value)
               << "\",\"minimum_q3_column\":\"" << decimal(q3_columns.value) << "\",\"minimum_q3_row\":\"" << decimal(q3_rows.value)
               << "\",\"elapsed_seconds\":" << seconds(started) << ",\"complete_domain\":false}\n";
        report.flush(); require(bool(report), "Field report write failed");
        std::cout << "PASS " << part << ' ' << lo << ' ' << hi << ' ' << pairs << ' ' << triples << '\n';
        return 0;
    } catch (const std::exception& e) {
        if (!out.empty()) refusal(out, e.what(), current);
        std::cerr << e.what() << '\n';
        return 2;
    }
}
