from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import RetrieveConnectionsParams, RetrieveConnectionsResult


class RetrieveConnections(Operation[RetrieveConnectionsParams, list[RetrieveConnectionsResult]]):
    """Retrieve standard LinkedIn connections."""

    operation_name = "retrieveConnections"
    mapper = ArrayWorkflowMapper[RetrieveConnectionsParams, RetrieveConnectionsResult](
        "st.retrieveConnections",
        RetrieveConnectionsResult,
    )
