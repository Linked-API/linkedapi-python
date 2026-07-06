from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvSyncInboxParams


class NvSyncInbox(Operation[NvSyncInboxParams, None]):
    """Enable whole-inbox monitoring for Sales Navigator conversations."""

    operation_name = "nvSyncInbox"
    mapper = VoidWorkflowMapper[NvSyncInboxParams]("nv.syncInbox")
