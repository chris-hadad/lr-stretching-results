# Same-input benchmark observations

Measured on 9 September 2026 with Python 3.14.3 on Darwin arm64.
One thread per fresh child, three repetitions per contender, alternating order.
Every paired count agrees exactly. The original and optimized implementations
have different pinned source hashes. There is no cross-call count cache.

## Transport and quotient counts

| Input | Original count time | Optimized count time | Count ratio | Contained ratio |
| --- | ---: | ---: | ---: | ---: |
| `transport-permutation10` | 0.000195 s | 0.000131 s | 1.50x | 0.97x |
| `transport-repeated3x8` | 0.004455 s | 0.001273 s | 3.50x | 1.00x |
| `native-chart-m0-t2` | 0.000240 s | 0.000198 s | 1.21x | 1.00x |
| `native-chart-m3-t4` | 0.007845 s | 0.001110 s | 7.07x | 0.99x |
| `transport-two-row` | 0.234137 s | 0.000060 s | 3932.37x | 3.09x |
| `transport-unequal` | 0.003163 s | 0.002149 s | 1.47x | 1.07x |
| `native-quotient-t10` | 0.000948 s | 0.000208 s | 4.56x | 1.09x |
| `quotient-unequal` | 0.000312 s | 0.000098 s | 3.17x | 0.96x |
| `quotient-repeated2x6` | 0.001876 s | 0.000845 s | 2.22x | 0.96x |
| `quotient-repeated4x3` | 0.000707 s | 0.000528 s | 1.34x | 0.97x |
| `mixed-star` | 0.000138 s | 0.000047 s | 2.93x | 0.90x |
| `mixed-star-transpose` | 0.000132 s | 0.000046 s | 2.88x | 1.02x |
| `transport-repeated8x8` | 5.728535 s | 1.664937 s | 3.44x | 3.27x |
| `quotient-repeated6x6` | 1.197487 s | 0.431165 s | 2.78x | 2.41x |

Ratios divide original time by optimized time; values below one are losses.
Count time excludes imports. Contained time includes interpreter startup,
serialization and cleanup, but excludes outer orchestration/report work. The
largest repeated-margin transport and quotient cases improve in both measures.
Most tiny cases are dominated by startup; some contained medians are slower.
The two-row formula removes a large enumeration, but its roughly four-thousand-
fold count-time ratio becomes about threefold at the complete child boundary.

The table contains fourteen exact inputs and eighty-four measurements. These
are shared-workstation observations, not a universal performance guarantee.
The raw per-repetition count time, contained time and process maximum RSS are
in [MEASUREMENTS.json](benchmarks/MEASUREMENTS.json). RSS includes the interpreter;
it is not an isolated allocation total for the algorithm.

## Three strip algorithms on the same proved whole objects

| Object | Grouped enumeration | Positive rational expansion | Integer moments |
| --- | ---: | ---: | ---: |
| `strip-old` | 3.40850025 s | 0.00021583 s | 0.00003362 s |
| `strip-neighbor` | 0.00497871 s | 0.00007808 s | 0.00002946 s |

The original-cone object is evaluated at stretch 1000; its neighbor at 100.
The eighteen corrected comparison measurements load both implementations
before starting the count timer. All three algorithms produce the same exact
integer on each object. The first, unequal-setup timing version and profile
runs are excluded. Both complete degree-ten coefficient vectors separately
agree with archived independent whole-hive Normaliz vectors, and four fresh
bare LR controls agree at stretches one and two.

The integer formula uses at most twice the number of composition coordinates
in binomial terms. Its arithmetic-operation count is independent of stretch
magnitude; integer bit complexity and dimension remain relevant. The separate
positive expansion supplies the positivity proof, while the exact integer
formula is the faster evaluator.

## Reproduce or adapt the comparison

```sh
python3 -B tooling/benchmarks/compare.py --case transport-repeated8x8 --repetitions 3
python3 -B tooling/benchmarks/compare.py --case native-chart-m3-t4
```

The bundled command reproduces the transport/quotient comparisons against the
frozen previous implementation. Each child has a timeout and each failure is
reported without a count. It measures its own subprocess overhead, which is
not identical to the original contained-observer overhead. The native chart
names identify prior native research inputs; this benchmark executes Python
algorithms and is not a fresh native LR or Barvinok run.

Algorithm choices, unsuccessful comparisons and remaining limits are explicit:
equal-cap orbit aggregation, bounded-composition prefix sums versus grouped
inclusion-exclusion, and mixed-star prefix moments versus numerator expansion.
No schedule cache was added: the measured improvements did not require one.
These tools do not accelerate every arbitrary LR or high-degree native cohort.
