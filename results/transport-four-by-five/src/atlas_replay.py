"""Recompute all 392 full degree-twelve arrays from labeled-edge counts."""
from pathlib import Path
import json, sys, time
import transport_math as m
from portable_io import save


def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for transport atlas replay')
    source, out = map(Path, sys.argv[1:])
    expected = json.loads(source.read_text())
    assert expected['degree_bound'] == 12
    expected_arrays = expected['newton_arrays']
    assert set(expected_arrays) == {m.occupation_key(o) for o in m.compositions(5, 4)}
    sites = m.sites()
    holds = ((13, 0, 0), (0, 0, 13))
    arrays = {}
    start = time.monotonic()
    for occupation in m.compositions(5, 4):
        key = m.occupation_key(occupation)
        targets = [m.strict_site(c, s) for c in range(7) for s in sites + holds]
        values, work = m.repeated_edge_counts(occupation, targets)
        assert work['labeled_edges'] == 15 and work['edge_rank'] == 3
        primary = []
        for chamber in range(7):
            counted = values[chamber * 457:(chamber + 1) * 457]
            coefficients = list(m.newton_from_values(counted[:455]))
            primary.append({'chamber': chamber, 'determining_counts': counted[:455],
                            'newton': coefficients, 'holdout_counts': counted[455:]})
        save(out / ('primary-' + key + '.json'), {'occupation': occupation, 'chambers': primary})
        for chamber, row in enumerate(primary):
            assert row['newton'] == expected_arrays[key][chamber]
            for point, value in zip(holds, row['holdout_counts']):
                assert m.newton_value(row['newton'], point) == value
        arrays[key] = [row['newton'] for row in primary]
    assert len(arrays) == 56
    save(out / 'atlas.json', {'degree_bound': 12, 'newton_arrays': arrays})
    save(out / 'RESULT.json', {'status': 'PASS', 'arrays': 392,
         'determining_values': 178360, 'unused_values': 784,
         'seconds': time.monotonic() - start})


if __name__ == '__main__':
    main()
