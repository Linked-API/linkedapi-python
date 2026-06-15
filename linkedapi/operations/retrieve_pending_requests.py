from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import RetrievePendingRequestsResult


class RetrievePendingRequests(Operation[None, list[RetrievePendingRequestsResult]]):
    """Retrieve pending standard LinkedIn connection requests."""

    operation_name = "retrievePendingRequests"
    mapper = ArrayWorkflowMapper[None, RetrievePendingRequestsResult](
        "st.retrievePendingRequests",
        RetrievePendingRequestsResult,
    )
