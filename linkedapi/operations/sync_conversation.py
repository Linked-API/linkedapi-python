from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import SyncConversationParams, SyncConversationResult


class SyncConversation(Operation[SyncConversationParams, SyncConversationResult]):
    """Sync a standard LinkedIn conversation."""

    operation_name = "syncConversation"
    mapper = SimpleWorkflowMapper[SyncConversationParams, SyncConversationResult](
        "st.syncConversation",
        result_model=SyncConversationResult,
    )
