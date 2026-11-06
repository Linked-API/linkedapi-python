from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvSaveLeadParams


class NvSaveLead(Operation[NvSaveLeadParams, None]):
    """Ensure a lead is saved; with listId, also ensure membership in that one list, leaving other
    lists untouched. Without listId, leave lists unchanged. Repeating succeeds without
    changes. Saving a lead may also save its current company in Sales Navigator. Current
    limitation: If you have more than 10 lead lists, Sales Navigator shows ten lists at a
    time. If the requested list is not shown, the call fails with unexpectedError. The lead
    may already be saved, but not added to that list.
    """

    operation_name = "nvSaveLead"
    mapper = VoidWorkflowMapper[NvSaveLeadParams]("nv.saveLead")
