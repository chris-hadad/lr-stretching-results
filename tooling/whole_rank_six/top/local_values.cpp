// Fresh independent exact normal-image-lattice recurrence for Pro028 intake.
// Inputs are local cones, never whole LR candidates. No provider code is linked.
#include <gmpxx.h>
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Q = mpq_class;
using Z = mpz_class;
using Row = std::vector<long>;
using IntMatrix = std::vector<Row>;
using Matrix = std::vector<std::vector<Q>>;
using Poly = std::array<Q, 7>;

void require(bool ok, const char* message) {
    if (!ok) throw std::runtime_error(message);
}

long integer(const Z& z) {
    require(z.fits_slong_p(), "integer overflow");
    return z.get_si();
}

// Unimodular column Euclid leaves a lower triangular basis of the column image.
long image_index(const IntMatrix& rows) {
    if (rows.empty()) return 1;
    const int q = rows.size(), m = rows[0].size();
    std::vector<std::vector<Z>> a(q, std::vector<Z>(m));
    for (int i = 0; i < q; ++i)
        for (int j = 0; j < m; ++j) a[i][j] = rows[i][j];
    Z result = 1;
    for (int k = 0; k < q; ++k) {
        int p = k;
        while (p < m && a[k][p] == 0) ++p;
        require(p < m, "dependent input normals");
        for (int i = 0; i < q; ++i) std::swap(a[i][k], a[i][p]);
        for (int j = k + 1; j < m; ++j) {
            while (a[k][j] != 0) {
                Z quotient = a[k][k] / a[k][j];
                for (int i = 0; i < q; ++i) {
                    a[i][k] -= quotient * a[i][j];
                    std::swap(a[i][k], a[i][j]);
                }
            }
        }
        result *= abs(a[k][k]);
    }
    return integer(result);
}

Matrix inverse(const Matrix& source) {
    const int n = source.size();
    Matrix a(n, std::vector<Q>(2*n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) a[i][j] = source[i][j];
        a[i][n+i] = 1;
    }
    for (int k = 0; k < n; ++k) {
        int p = k;
        while (p < n && a[p][k] == 0) ++p;
        require(p < n, "singular Gram matrix");
        std::swap(a[p], a[k]);
        Q pivot = a[k][k];
        for (int j = 0; j < 2*n; ++j) a[k][j] /= pivot;
        for (int i = 0; i < n; ++i) if (i != k) {
            Q scale = a[i][k];
            if (scale == 0) continue;
            for (int j = 0; j < 2*n; ++j) a[i][j] -= scale * a[k][j];
        }
    }
    Matrix out(n, std::vector<Q>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) out[i][j] = a[i][j+n];
    return out;
}

Poly multiply(const Poly& a, const Poly& b, int degree) {
    Poly c{};
    for (int i = 0; i <= degree; ++i) if (a[i] != 0)
        for (int j = 0; i+j <= degree; ++j) if (b[j] != 0)
            c[i+j] += a[i] * b[j];
    return c;
}

std::vector<int> bits(int mask, int q) {
    std::vector<int> result;
    for (int i = 0; i < q; ++i) if (mask & (1 << i)) result.push_back(i);
    return result;
}

struct LocalResult {
    Q alpha;
    long index;
    long numerator_points;
    long subtractions;
    int generic_seed;
};

LocalResult evaluate(const IntMatrix& normals, bool omit_sixth = false) {
    const int q = normals.size(), m = normals[0].size(), all = (1 << q)-1;
    require(q >= 1 && q <= 6 && m >= q && m <= 10, "input dimension outside contract");
    for (const auto& row: normals) {
        require((int)row.size() == m, "ragged normal matrix");
        for (long value: row) require(std::abs(value) <= 8, "normal entry bound");
    }
    const long full_index = image_index(normals);
    require(full_index >= 1 && full_index <= 64, "normal index bound");
    IntMatrix gram(q, Row(q));
    for (int i = 0; i < q; ++i)
        for (int j = 0; j < q; ++j)
            for (int k = 0; k < m; ++k) gram[i][j] += normals[i][k]*normals[j][k];
    std::vector<long> indices(all+1, 1);
    std::vector<std::vector<int>> selected(all+1);
    std::vector<Matrix> inverses(all+1);
    for (int mask = 1; mask <= all; ++mask) {
        selected[mask] = bits(mask, q);
        const auto& chosen = selected[mask];
        IntMatrix rows;
        Matrix g(chosen.size(), std::vector<Q>(chosen.size()));
        for (int i: chosen) rows.push_back(normals[i]);
        // Index-one full row lattice implies every row sublattice is saturated.
        if (full_index != 1) indices[mask] = image_index(rows);
        for (size_t i = 0; i < chosen.size(); ++i)
            for (size_t j = 0; j < chosen.size(); ++j) g[i][j] = gram[chosen[i]][chosen[j]];
        inverses[mask] = inverse(g);
    }
    require(indices[all] == full_index, "index consistency");
    std::vector<std::vector<Q>> covectors(all+1);
    int seed = 0;
    for (int base = 2; base <= 129; ++base) {
        bool good = true;
        std::vector<Z> w(q, 1);
        for (int i = 1; i < q; ++i) w[i] = w[i-1]*base;
        for (int mask = 1; mask <= all && good; ++mask) {
            const auto& chosen = selected[mask];
            std::vector<Q> c(chosen.size());
            for (size_t i = 0; i < chosen.size(); ++i) {
                for (size_t j = 0; j < chosen.size(); ++j)
                    c[i] += inverses[mask][i][j] * w[chosen[j]];
                if (c[i] == 0) good = false;
            }
            covectors[mask] = std::move(c);
        }
        if (good) { seed = base; break; }
    }
    require(seed != 0, "generic specialization exhausted");
    std::vector<Poly> mu(all+1);
    mu[0][0] = 1;
    long point_count = 0, subtraction_count = 0;
    for (int mask = 1; mask <= all; ++mask) {
        const auto& chosen = selected[mask];
        const auto& c = covectors[mask];
        const int n = chosen.size();
        Row lengths(n);
        long box = 1;
        for (int i = 0; i < n; ++i) {
            const int child = mask ^ (1 << chosen[i]);
            require(indices[mask] % indices[child] == 0, "nonintegral primitive axis");
            lengths[i] = indices[mask]/indices[child];
            box *= lengths[i];
        }
        require(box % indices[mask] == 0 && box/indices[mask] <= 4096, "numerator bound");
        std::vector<Row> residues(1, Row(n));
        std::set<Row> seen{residues[0]};
        for (size_t cursor = 0; cursor < residues.size(); ++cursor) {
            for (int col = 0; col < m; ++col) {
                Row next(n);
                for (int i = 0; i < n; ++i) {
                    long value = (residues[cursor][i]+normals[chosen[i]][col]) % lengths[i];
                    next[i] = value < 0 ? value+lengths[i] : value;
                }
                if (seen.insert(next).second) residues.push_back(std::move(next));
            }
            require(residues.size() <= (size_t)(box/indices[mask]), "residue closure exceeds index");
        }
        require(residues.size() == (size_t)(box/indices[mask]), "incomplete numerator");
        point_count += residues.size();
        Poly numerator{};
        for (const auto& point: residues) {
            Q v = 0;
            for (int i = 0; i < n; ++i) v += c[i]*point[i];
            Q term = 1;
            for (int k = 0; k <= q; ++k) {
                if (k) term *= v/k;
                numerator[k] += term;
            }
        }
        Poly series = numerator;
        for (int i = 0; i < n; ++i) {
            const Q a = lengths[i]*c[i];
            Poly factor{};
            factor[0] = -1/a;
            factor[1] = Q(1,2);
            factor[2] = -a/12;
            factor[4] = a*a*a/720;
            if (!omit_sixth) factor[6] = -a*a*a*a*a/30240;
            series = multiply(series, factor, q);
        }
        for (int removed = mask; removed; removed = (removed-1)&mask) {
            const int child = mask ^ removed;
            Q coefficient = Q(indices[child]) / Q(indices[mask]);
            for (int i = 0; i < n; ++i) if (removed & (1 << chosen[i])) coefficient /= -c[i];
            for (int k = 0; k <= q; ++k) series[k] -= coefficient*mu[child][k];
            ++subtraction_count;
        }
        for (int k = 0; k < n; ++k) require(series[k] == 0, "uncancelled Laurent pole");
        mu[mask] = std::move(series);
    }
    return {mu[all][q], full_index, point_count, subtraction_count, seed};
}

int main(int argc, char** argv) {
    try {
        const bool omit_sixth = argc == 2 && std::string(argv[1]) == "--omit-sixth-control";
        std::string label;
        int q, m;
        long declared_index;
        while (std::cin >> label) {
            require(bool(std::cin >> q >> m >> declared_index), "truncated or malformed input header");
            require(q >= 1 && q <= 6 && m >= q && m <= 10, "input header outside contract");
            IntMatrix n(q, Row(m));
            for (auto& row: n) for (auto& value: row) require(bool(std::cin >> value), "truncated normals");
            const auto start = std::chrono::steady_clock::now();
            const auto result = evaluate(n, omit_sixth);
            require(result.index == declared_index, "declared normal index mismatch");
            const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
            std::cout << label << ' ' << result.index << ' ' << result.alpha << ' '
                      << result.numerator_points << ' ' << result.subtractions << ' '
                      << result.generic_seed << ' ' << elapsed << '\n' << std::flush;
        }
        require(std::cin.eof(), "invalid trailing input");
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "REFUSED: " << e.what() << '\n';
        return 2;
    }
}
