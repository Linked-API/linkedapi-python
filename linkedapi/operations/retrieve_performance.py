from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import RetrievePerformanceResult


class RetrievePerformance(Operation[None, RetrievePerformanceResult]):
    """Retrieve LinkedIn performance metrics."""

    operation_name = "retrievePerformance"
    mapper = SimpleWorkflowMapper[None, RetrievePerformanceResult](
        "st.retrievePerformance",
        result_model=RetrievePerformanceResult,
    )
