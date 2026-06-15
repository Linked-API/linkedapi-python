from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import RetrieveSSIResult


class RetrieveSSI(Operation[None, RetrieveSSIResult]):
    """Retrieve LinkedIn SSI metrics."""

    operation_name = "retrieveSSI"
    mapper = SimpleWorkflowMapper[None, RetrieveSSIResult](
        "st.retrieveSSI",
        result_model=RetrieveSSIResult,
    )
