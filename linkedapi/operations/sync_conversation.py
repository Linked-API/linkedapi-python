from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import SyncConversationParams


class SyncConversation(Operation[SyncConversationParams, None]):
    """Sync a standard LinkedIn conversation."""

    operation_name = "syncConversation"
    mapper = VoidWorkflowMapper[SyncConversationParams]("st.syncConversation")
