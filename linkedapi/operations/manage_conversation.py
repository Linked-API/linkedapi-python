from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import ManageConversationParams


class ManageConversation(Operation[ManageConversationParams, None]):
    """Manage a standard LinkedIn conversation thread."""

    operation_name = "manageConversation"
    mapper = VoidWorkflowMapper[ManageConversationParams]("st.manageConversation")
