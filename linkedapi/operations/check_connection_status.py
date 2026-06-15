from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import CheckConnectionStatusParams, CheckConnectionStatusResult


class CheckConnectionStatus(Operation[CheckConnectionStatusParams, CheckConnectionStatusResult]):
    """Check a standard LinkedIn connection status."""

    operation_name = "checkConnectionStatus"
    mapper = SimpleWorkflowMapper[CheckConnectionStatusParams, CheckConnectionStatusResult](
        "st.checkConnectionStatus",
        result_model=CheckConnectionStatusResult,
    )
