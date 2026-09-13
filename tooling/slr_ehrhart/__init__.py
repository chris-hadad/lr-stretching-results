"""Standalone exact mathematical APIs; domain and proof contracts are in PROOFS.md."""
__version__ = "tooling-2026-09-12"
from .constructions import skew_content_to_lr, capped_matrix_to_lr
from .transport import (transport_count, transport_to_lr, minkowski_obstruction,
                        segment_quotient_count, segment_quotient_evaluate, segment_quotient_geometry)
from .strip import strip_count, strip_polynomial
from .flow_support import flow_support_certificate, verify_flow_support_certificate
from .cdagger import (OutsideCdaggerError, cdagger_parameters, cdagger_count,
                      cdagger_polynomial, verify_cdagger_certificate)
from .matrix_invariants import (MatrixCountLimitError, matrix_invariant_count,
                                rectangular_matrix_invariant_count, matrix_invariants_to_lr)
from .support import SupportPlan, plan_support
from .skew_count import SkewCountLimitError, skew_tableau_count
from .two_widths import two_width_count, two_width_polynomial
from .rank6_split import rank6_split_parameters, rank6_split_count, rank6_split_polynomial
from .rank8_clipped import rank8_clipped_boundary, rank8_clipped_count, rank8_clipped_polynomial

__all__ = [
    "skew_content_to_lr", "capped_matrix_to_lr",
    "transport_count", "transport_to_lr", "minkowski_obstruction",
    "segment_quotient_count", "segment_quotient_evaluate", "segment_quotient_geometry",
    "strip_count", "strip_polynomial",
    "flow_support_certificate", "verify_flow_support_certificate",
    "OutsideCdaggerError", "cdagger_parameters", "cdagger_count", "cdagger_polynomial",
    "verify_cdagger_certificate", "MatrixCountLimitError", "matrix_invariant_count",
    "rectangular_matrix_invariant_count", "matrix_invariants_to_lr",
    "SupportPlan", "plan_support", "SkewCountLimitError", "skew_tableau_count",
    "two_width_count", "two_width_polynomial", "rank6_split_parameters",
    "rank6_split_count", "rank6_split_polynomial", "rank8_clipped_boundary",
    "rank8_clipped_count", "rank8_clipped_polynomial",
]
