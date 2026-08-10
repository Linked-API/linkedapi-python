from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import NvSyncConversationParams, NvSyncConversationResult


class NvSyncConversation(Operation[NvSyncConversationParams, NvSyncConversationResult]):
    """Sync a Sales Navigator conversation."""

    operation_name = "nvSyncConversation"
    mapper = SimpleWorkflowMapper[NvSyncConversationParams, NvSyncConversationResult](
        "nv.syncConversation",
        result_model=NvSyncConversationResult,
    )
