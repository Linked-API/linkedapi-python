from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import SyncInboxParams


class SyncInbox(Operation[SyncInboxParams, None]):
    """Enable whole-inbox monitoring for standard LinkedIn conversations."""

    operation_name = "syncInbox"
    mapper = VoidWorkflowMapper[SyncInboxParams]("st.syncInbox")
