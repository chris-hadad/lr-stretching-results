"""Small exact examples; prints JSON and writes no files."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from slr_ehrhart import (
    cdagger_count, cdagger_polynomial, flow_support_certificate,
    matrix_invariant_count, segment_quotient_count, skew_content_to_lr, skew_tableau_count,
    transport_count, verify_cdagger_certificate, verify_flow_support_certificate,
)


def main():
    triple = ([43, 38, 33, 20, 12, 6], [22, 17, 16, 12, 6], [26, 21, 16, 12, 4])
    certificate = flow_support_certificate([(0, 1), (0, 2), (1, 2)], [1, 1])
    verify_flow_support_certificate([(0, 1), (0, 2), (1, 2)], [1, 1], certificate)
    result = {
        'cdagger_count_at_one': cdagger_count(*triple),
        'cdagger_ordinary_coefficients': [str(value) for value in cdagger_polynomial(*triple)],
        'cdagger_certificate': verify_cdagger_certificate(),
        'transport_count': transport_count([2, 2, 1, 1], [2, 2, 1, 1]),
        'quotient_at_two': segment_quotient_count([1, 1], [1, 1], 2),
        'flow_fiber_degree': certificate['degree'],
        'skew_lift': {key: value for key, value in skew_content_to_lr([2, 1], [1], [1, 1]).items()
                      if key != 'metadata'},
        'matrix_invariant_count': matrix_invariant_count(2, 4, 2),
        'rank13_skew_count_at_two': skew_tableau_count([30, 26, 3, 2, 1], [2, 1], [14, 14, 14, 12, 1, 1, 1, 1, 1], 2),
        'native_skew_count': skew_tableau_count([5, 4, 3, 2, 1], [2, 1, 1], [2, 2, 2, 1, 1, 1, 1, 1]),
    }
    if (result['cdagger_count_at_one'], result['transport_count'], result['quotient_at_two'],
            result['flow_fiber_degree'], result['matrix_invariant_count']) != (4590, 58, 376, 1, 56):
        raise ValueError('an exact quickstart control disagrees')
    if result['rank13_skew_count_at_two'] != 12562151868 or result['native_skew_count'] != 4576:
        raise ValueError('a skew-count control disagrees')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
