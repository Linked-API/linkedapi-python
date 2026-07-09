from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import IgnoreConnectionRequestParams


class IgnoreConnectionRequest(Operation[IgnoreConnectionRequestParams, None]):
    """Ignore an incoming standard LinkedIn connection request."""

    operation_name = "ignoreConnectionRequest"
    mapper = VoidWorkflowMapper[IgnoreConnectionRequestParams]("st.ignoreConnectionRequest")
