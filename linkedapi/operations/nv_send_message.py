from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvSendMessageParams


class NvSendMessage(Operation[NvSendMessageParams, None]):
    """Send a Sales Navigator message."""

    operation_name = "nvSendMessage"
    mapper = VoidWorkflowMapper[NvSendMessageParams]("nv.sendMessage")
