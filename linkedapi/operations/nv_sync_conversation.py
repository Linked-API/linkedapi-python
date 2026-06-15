from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvSyncConversationParams


class NvSyncConversation(Operation[NvSyncConversationParams, None]):
    """Sync a Sales Navigator conversation."""

    operation_name = "nvSyncConversation"
    mapper = VoidWorkflowMapper[NvSyncConversationParams]("nv.syncConversation")
