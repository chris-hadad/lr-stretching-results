// Independently derived lower cover: supporting faces, pulling, and exact volume.
#include "common.hpp"
using namespace lf;

mpz_class determinant(const std::vector<Ray>& vertices) {
    require(vertices.size() == 8, "Simplex does not have eight vertices");
    std::array<std::array<mpz_class, 8>, 8> a;
    for (int i = 0; i < 8; ++i) for (int j = 0; j < 8; ++j) a[i][j] = mpz_class(std::to_string(vertices[i][j]));
    mpz_class previous = 1;
    int sign = 1;
    for (int k = 0; k < 7; ++k) {
        int p = k;
        while (p < 8 && a[p][k] == 0) ++p;
        if (p == 8) return 0;
        if (p != k) { std::swap(a[p], a[k]); sign = -sign; }
        mpz_class pivot = a[k][k];
        for (int i = k + 1; i < 8; ++i) for (int j = k + 1; j < 8; ++j) {
            mpz_class value = a[i][j] * pivot - a[i][k] * a[k][j];
            require(mpz_divisible_p(value.get_mpz_t(), previous.get_mpz_t()), "Nonexact Bareiss division");
            mpz_divexact(a[i][j].get_mpz_t(), value.get_mpz_t(), previous.get_mpz_t());
        }
        for (int i = k + 1; i < 8; ++i) a[i][k] = 0;
        previous = pivot;
    }
    return sign * a[7][7];
}

struct Pulling {
    const State& state;
    const std::vector<int>& ids;
    std::vector<U> supporting;
    std::map<U, std::vector<std::vector<int>>> cache;
    I face_rank_checks = 0;

    Pulling(const State& state_, const std::vector<int>& ids_) : state(state_), ids(ids_) {
        require(rank_mod(vertex_rows(state, ids, all_bits(ids.size()))) == 8,
                "Cell full dimension lacks an exact rank witness");
        if (ids.size() == 8) return;
        std::set<U> unique;
        for (int h = 0; h < 219; ++h) {
            U active = 0;
            for (size_t i = 0; i < ids.size(); ++i)
                if ((state.signs[ids[i]].zero[h / 64] >> (h % 64)) & 1) active |= U(1) << i;
            if (popcount(active) < 7 || active == all_bits(ids.size())) continue;
            ++face_rank_checks;
            if (rank_mod(vertex_rows(state, ids, active)) == 7) unique.insert(active);
        }
        supporting.assign(unique.begin(), unique.end());
        require(!supporting.empty(), "No supporting facets found for nonsimplicial cell");
    }

    const std::vector<std::vector<int>>& run(U face, int homogeneous_rank) {
        auto found = cache.find(face);
        if (found != cache.end()) return found->second;
        std::set<std::vector<int>> simplices;
        if (popcount(face) == homogeneous_rank) {
            std::vector<int> simplex;
            for (size_t i = 0; i < ids.size(); ++i) if (face & (U(1) << i)) simplex.push_back(ids[i]);
            simplices.insert(std::move(simplex));
        } else {
            int apex = first_bit(face);
            std::set<U> faces;
            for (U supporting_face : supporting) {
                U candidate = face & supporting_face;
                if (!candidate || candidate == face || (candidate & (U(1) << apex))
                    || popcount(candidate) < homogeneous_rank - 1) continue;
                ++face_rank_checks;
                // The proper supporting intersection bounds rank above by r-1;
                // this modular witness proves rank at least r-1 over Q.
                if (rank_mod(vertex_rows(state, ids, candidate)) == homogeneous_rank - 1) faces.insert(candidate);
            }
            for (U next : faces) for (const auto& base : run(next, homogeneous_rank - 1)) {
                auto simplex = base;
                simplex.push_back(ids[apex]);
                std::sort(simplex.begin(), simplex.end());
                require(std::adjacent_find(simplex.begin(), simplex.end()) == simplex.end(), "Repeated pulling apex");
                simplices.insert(std::move(simplex));
            }
            require(!simplices.empty(), "Pulling lower cover lost an entire positive-dimensional face");
        }
        auto result = cache.emplace(face, std::vector<std::vector<int>>(simplices.begin(), simplices.end()));
        return result.first->second;
    }
};

uint64_t signature_word(std::istream& input) {
    std::string word;
    require(bool(input >> word) && !word.empty(), "Missing sign word");
    require(std::all_of(word.begin(), word.end(), [](char c) { return c >= '0' && c <= '9'; }), "Malformed unsigned sign word");
    size_t consumed = 0;
    uint64_t result = std::stoull(word, &consumed);
    require(consumed == word.size(), "Trailing sign characters");
    return result;
}

int main(int argc, char** argv) {
    std::string out;
    I current = -1;
    try {
        require(argc == 10, "Expected state-U state-F part lo hi cells simplices signs output");
        out = argv[9];
        require(std::filesystem::is_directory(out), "Runner output directory is missing");
        char part = std::string(argv[3]).at(0);
        require(std::string(argv[3]).size() == 1, "Malformed part");
        I lo = argument_integer(argv[4]), hi = argument_integer(argv[5]);
        auto started = std::chrono::steady_clock::now();
        State state = read_state(part == 'U' ? argv[1] : argv[2], part, lo, hi);
        State other = read_state(part == 'U' ? argv[2] : argv[1], part == 'U' ? 'F' : 'U', 0, 1);
        mpz_class lcm = 1;
        for (const auto* s : {&state, &other}) for (const Ray& v : s->vertices)
            mpz_lcm_ui(lcm.get_mpz_t(), lcm.get_mpz_t(), static_cast<unsigned long>(v[7]));
        mpz_class denominator;
        mpz_pow_ui(denominator.get_mpz_t(), lcm.get_mpz_t(), 8);
        std::ifstream cells(argv[6]), simplices(argv[7]), signs(argv[8]);
        require(bool(cells) && bool(simplices) && bool(signs), "Missing cover input");
        I first = integer(cells, "cover first"), last = integer(cells, "cover last");
        std::string den_text;
        require(bool(cells >> den_text), "Missing cover denominator");
        mpz_class supplied_denominator(den_text);
        require(first >= 0 && first <= lo && hi <= last && last <= state.total, "Cover interval differs");
        require(supplied_denominator == denominator, "Cover denominator differs from independent vertex lcm");
        auto signatures_out = fresh(std::filesystem::path(out) / "signatures.bin", true);
        auto volume_out = fresh(std::filesystem::path(out) / "volumes.txt");
        auto simplex_out = fresh(std::filesystem::path(out) / "simplices.txt");
        auto determinant_out = fresh(std::filesystem::path(out) / "determinants.txt");
        std::set<Signature> distinct;
        mpz_class total_numerator = 0, max_determinant = 0;
        I total_simplices = 0, rank_checks = 0, nonunimodular = 0;
        for (I id = first; id < hi; ++id) {
            I cid = integer(cells, "cover cell id"), nv = integer(cells, "cover vertex count");
            I ns = integer(cells, "cover simplex count");
            std::string numerator_text;
            require(bool(cells >> numerator_text), "Missing cell volume");
            mpz_class expected_volume(numerator_text);
            require(cid == id && nv >= 8 && nv <= 128 && ns > 0 && ns <= 1000000 && expected_volume > 0,
                    "Invalid cover cell header");
            I sid = integer(simplices, "simplex cell id"), sn = integer(simplices, "simplex count");
            require(sid == id && sn == ns, "Simplex cell identity or count differs");
            std::vector<std::vector<int>> returned;
            for (I j = 0; j < ns; ++j) {
                std::vector<int> simplex;
                for (int k = 0; k < 8; ++k) {
                    I v = integer(simplices, "simplex vertex");
                    require(v >= 0 && v < I(state.vertices.size()), "Simplex vertex outside state");
                    simplex.push_back(int(v));
                }
                std::sort(simplex.begin(), simplex.end());
                require(std::adjacent_find(simplex.begin(), simplex.end()) == simplex.end(), "Degenerate returned simplex roster");
                returned.push_back(std::move(simplex));
            }
            require(integer(signs, "sign cell id") == id, "Sign cell identity differs");
            Signature source_signs;
            for (auto& word : source_signs) word = signature_word(signs);
            require((source_signs[3] >> 18) == 0, "Trailing cut-sign bits");
            if (id < lo) continue;
            current = id;
            const auto& cell = state.cells[size_t(id - lo)];
            require(I(cell.size()) == nv, "Cover cell vertex population differs");
            Signature actual_signs = cell_signature(state, cell);
            require(actual_signs == source_signs, "Independent strict cut signs disagree");
            require(distinct.insert(actual_signs).second, "Duplicate strict sign within cover batch");
            Pulling pulling(state, cell);
            const auto& independent = pulling.run(all_bits(cell.size()), 8);
            std::sort(returned.begin(), returned.end());
            require(std::adjacent_find(returned.begin(), returned.end()) == returned.end(), "Duplicate returned simplex");
            require(returned == independent, "Independent pulling simplex roster disagrees");
            mpz_class cell_volume = 0;
            simplex_out << id << ' ' << independent.size();
            determinant_out << id << ' ' << independent.size();
            for (const auto& simplex : independent) {
                std::vector<Ray> vertices;
                mpz_class product = 1;
                for (int index : simplex) {
                    require(std::binary_search(cell.begin(), cell.end(), index), "Simplex escapes its cell vertex set");
                    vertices.push_back(state.vertices[index]);
                    product *= static_cast<unsigned long>(state.vertices[index][7]);
                    simplex_out << ' ' << index;
                }
                mpz_class det = determinant(vertices);
                if (det < 0) det = -det;
                require(det > 0, "Singular pulling simplex");
                require(mpz_divisible_p(denominator.get_mpz_t(), product.get_mpz_t()), "Simplex denominator does not divide independent common denominator");
                mpz_class factor;
                mpz_divexact(factor.get_mpz_t(), denominator.get_mpz_t(), product.get_mpz_t());
                cell_volume += det * factor;
                if (det > max_determinant) max_determinant = det;
                nonunimodular += det != 1;
                determinant_out << ' ' << det;
            }
            simplex_out << '\n';
            determinant_out << '\n';
            volume_out << id << ' ' << nv << ' ' << independent.size() << ' ' << cell_volume << '\n';
            require(cell_volume == expected_volume, "Exact cell volume disagrees");
            put_i64(signatures_out, id);
            for (uint64_t word : actual_signs) put_u64(signatures_out, word);
            total_numerator += cell_volume;
            total_simplices += I(independent.size());
            rank_checks += pulling.face_rank_checks;
        }
        if (hi == last) { eof(cells, "cover cells"); eof(simplices, "cover simplices"); eof(signs, "cover signs"); }
        for (auto* f : {&volume_out, &simplex_out, &determinant_out, &signatures_out}) {
            f->flush(); require(bool(*f), "Independent geometry output failed");
        }
        auto report = fresh(std::filesystem::path(out) / "COVER-BATCH.json");
        report << "{\"schema\":\"pro030-independent-cover-batch/v1\",\"status\":\"PASS\",\"part\":\"" << part
               << "\",\"lo\":" << lo << ",\"hi\":" << hi << ",\"cells\":" << hi - lo
               << ",\"simplices\":" << total_simplices << ",\"strict_signatures\":" << distinct.size()
               << ",\"rank_witnesses\":" << rank_checks << ",\"volume_numerator\":\"" << total_numerator
               << "\",\"denominator\":\"" << denominator << "\",\"vertex_denominator_lcm\":\"" << lcm
               << "\",\"maximum_homogeneous_determinant\":\"" << max_determinant
               << "\",\"nonunimodular_simplices\":" << nonunimodular
               << ",\"elapsed_seconds\":" << seconds(started) << ",\"complete_domain\":false}\n";
        report.flush(); require(bool(report), "Geometry report write failed");
        std::cout << "PASS " << part << ' ' << lo << ' ' << hi << ' ' << total_simplices << '\n';
        return 0;
    } catch (const std::exception& e) {
        if (!out.empty()) refusal(out, e.what(), current);
        std::cerr << e.what() << '\n';
        return 2;
    }
}
