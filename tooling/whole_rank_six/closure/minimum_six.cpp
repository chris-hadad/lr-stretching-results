#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

using Mask = std::uint64_t;
constexpr Mask ALL = (Mask(1) << 45) - 1;
std::vector<std::pair<Mask,Mask>> rules;
std::vector<Mask> zero_sets;
std::array<std::uint64_t,6> counts{};

void need(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

Mask old_closure(Mask seed) {
    for (;;) {
        const Mask before = seed;
        for (const auto& rule : rules)
            if ((seed & rule.first) == rule.first) seed |= rule.second;
        if (seed == before) return seed;
    }
}

void check(Mask seed, unsigned cardinality) {
    Mask witness_closure = ALL;
    for (Mask zeros : zero_sets)
        if ((seed & zeros) == seed) witness_closure &= zeros;
    if (old_closure(seed) != witness_closure) {
        std::cerr << "counterexample seed mask " << seed << '\n';
        throw std::runtime_error("a smaller closure discrepancy exists");
    }
    ++counts[cardinality];
}

void enumerate(unsigned next, unsigned left, unsigned cardinality, Mask seed) {
    if (left == 0) { check(seed, cardinality); return; }
    for (unsigned i = next; i + left <= 45; ++i)
        enumerate(i + 1, left - 1, cardinality, seed | (Mask(1) << i));
}

int main(int argc, char** argv) {
    try {
        need(argc == 2, "usage: minimum_six EXHAUSTION.txt");
        const auto start = std::chrono::steady_clock::now();
        std::ifstream input(argv[1]);
        unsigned variables = 0, rule_count = 0, point_count = 0;
        input >> variables >> rule_count >> point_count;
        need(bool(input) && variables == 45 && rule_count == 204 && point_count == 166,
             "complete declared finite instance");
        for (unsigned i = 0; i < rule_count; ++i) {
            Mask a = 0, b = 0; input >> a >> b;
            need(bool(input) && a && b && a <= ALL && b <= ALL, "positive rule masks");
            rules.emplace_back(a,b);
        }
        for (unsigned i = 0; i < point_count; ++i) {
            Mask value = 0; input >> value;
            need(bool(input) && value <= ALL, "feasible-witness mask");
            zero_sets.push_back(value);
        }
        input >> std::ws; need(input.eof(), "unexpected trailing input");
        for (unsigned k = 0; k <= 5; ++k) enumerate(0,k,k,0);
        const std::array<std::uint64_t,6> expected{{1,45,990,14190,148995,1221759}};
        need(counts == expected, "complete combination populations");
        std::uint64_t total = 0;
        for (auto n : counts) total += n;
        need(total == 1385980, "complete seed count");
        std::cout << "{\"status\":\"PASS_COMPLETE_MINIMUM_SIX_EXHAUSTION\","
                  << "\"scope\":\"all original seeds of cardinality zero through five; "
                     "requires separately verified exact closure certificate and six-row countermodel\","
                  << "\"seeds\":" << total << ",\"counts\":[";
        for (unsigned i = 0; i < counts.size(); ++i) {
            if (i) std::cout << ',';
            std::cout << counts[i];
        }
        std::cout << "],\"seconds\":"
                  << std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()
                  << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "REFUSED: " << error.what() << '\n';
        return 2;
    }
}
