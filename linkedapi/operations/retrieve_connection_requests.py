from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import RetrieveConnectionRequestsResult


class RetrieveConnectionRequests(Operation[None, list[RetrieveConnectionRequestsResult]]):
    """Retrieve incoming standard LinkedIn connection requests."""

    operation_name = "retrieveConnectionRequests"
    mapper = ArrayWorkflowMapper[None, RetrieveConnectionRequestsResult](
        "st.retrieveConnectionRequests",
        RetrieveConnectionRequestsResult,
    )
