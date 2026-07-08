from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import AcceptConnectionRequestParams


class AcceptConnectionRequest(Operation[AcceptConnectionRequestParams, None]):
    """Accept an incoming standard LinkedIn connection request."""

    operation_name = "acceptConnectionRequest"
    mapper = VoidWorkflowMapper[AcceptConnectionRequestParams]("st.acceptConnectionRequest")
