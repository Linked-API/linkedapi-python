from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SendMessageMapper
from linkedapi.types import SendMessageParams


class SendMessage(Operation[SendMessageParams, None]):
    """Send a standard LinkedIn message."""

    operation_name = "sendMessage"
    mapper = SendMessageMapper()
