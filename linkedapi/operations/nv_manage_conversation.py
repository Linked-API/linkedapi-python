from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvManageConversationParams


class NvManageConversation(Operation[NvManageConversationParams, None]):
    """Manage a Sales Navigator conversation thread."""

    operation_name = "nvManageConversation"
    mapper = VoidWorkflowMapper[NvManageConversationParams]("nv.manageConversation")
