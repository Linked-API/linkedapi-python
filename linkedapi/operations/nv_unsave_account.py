from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvUnsaveAccountParams


class NvUnsaveAccount(Operation[NvUnsaveAccountParams, None]):
    """Unsave the account only; its saved leads stay saved. Repeating succeeds without changes."""

    operation_name = "nvUnsaveAccount"
    mapper = VoidWorkflowMapper[NvUnsaveAccountParams]("nv.unsaveAccount")
