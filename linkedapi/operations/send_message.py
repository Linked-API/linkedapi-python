from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import SendMessageParams


class SendMessage(Operation[SendMessageParams, None]):
    """Send a standard LinkedIn message."""

    operation_name = "sendMessage"
    mapper = VoidWorkflowMapper[SendMessageParams]("st.sendMessage")
