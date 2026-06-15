from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import RemoveConnectionParams


class RemoveConnection(Operation[RemoveConnectionParams, None]):
    """Remove a standard LinkedIn connection."""

    operation_name = "removeConnection"
    mapper = VoidWorkflowMapper[RemoveConnectionParams]("st.removeConnection")
