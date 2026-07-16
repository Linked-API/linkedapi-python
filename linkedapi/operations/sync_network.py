from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import SyncNetworkParams


class SyncNetwork(Operation[SyncNetworkParams, None]):
    """Enable whole-network monitoring for standard LinkedIn connections."""

    operation_name = "syncNetwork"
    mapper = VoidWorkflowMapper[SyncNetworkParams]("st.syncNetwork")
