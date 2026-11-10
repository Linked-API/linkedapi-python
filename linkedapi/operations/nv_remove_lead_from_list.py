from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvRemoveLeadFromListParams


class NvRemoveLeadFromList(Operation[NvRemoveLeadFromListParams, None]):
    """Remove a lead from exactly one owned custom list, keeping it saved and in its other
    lists. Repeating an absent membership succeeds.
    """

    operation_name = "nvRemoveLeadFromList"
    mapper = VoidWorkflowMapper[NvRemoveLeadFromListParams]("nv.removeLeadFromList")
