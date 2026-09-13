"""Versioned standard-library projection of the maintained exact mathematical tools."""
__version__ = "shared-tools-2026-09-09.2"
from .constructions import skew_content_to_lr, capped_matrix_to_lr
from .transport import (transport_count, transport_to_lr, minkowski_obstruction,
                        segment_quotient_count, segment_quotient_evaluate, segment_quotient_geometry)
from .strip import strip_count, strip_polynomial
from .flow_support import flow_support_certificate, verify_flow_support_certificate
from .cdagger import (OutsideCdaggerError, cdagger_parameters, cdagger_count,
                      cdagger_polynomial, verify_cdagger_certificate)
from .matrix_invariants import MatrixCountLimitError, matrix_invariant_count, matrix_invariants_to_lr
from .support import SupportPlan, plan_support
from .skew_count import SkewCountLimitError, skew_tableau_count
