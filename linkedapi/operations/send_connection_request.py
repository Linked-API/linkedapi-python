from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import SendConnectionRequestParams


class SendConnectionRequest(Operation[SendConnectionRequestParams, None]):
    """Send a standard LinkedIn connection request."""

    operation_name = "sendConnectionRequest"
    mapper = VoidWorkflowMapper[SendConnectionRequestParams]("st.sendConnectionRequest")
