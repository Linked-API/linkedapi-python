from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvSaveAccountParams


class NvSaveAccount(Operation[NvSaveAccountParams, None]):
    """Ensure an account is saved and optionally in one list, leaving other lists untouched.
    Without listId, leave lists unchanged. Repeating succeeds without changes. Current
    limitation: If you have more than 10 account lists, Sales Navigator shows ten lists at a
    time. If the requested list is not shown, the call fails with unexpectedError. The
    account may already be saved, but not added to that list.
    """

    operation_name = "nvSaveAccount"
    mapper = VoidWorkflowMapper[NvSaveAccountParams]("nv.saveAccount")
