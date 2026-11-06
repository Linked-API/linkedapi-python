from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvUnsaveLeadParams


class NvUnsaveLead(Operation[NvUnsaveLeadParams, None]):
    """Use Sales Navigator's native unsave: the lead is no longer saved and leaves every custom list
    the user owns. Repeating succeeds without changes."""

    operation_name = "nvUnsaveLead"
    mapper = VoidWorkflowMapper[NvUnsaveLeadParams]("nv.unsaveLead")
