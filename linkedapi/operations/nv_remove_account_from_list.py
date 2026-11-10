from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvRemoveAccountFromListParams


class NvRemoveAccountFromList(Operation[NvRemoveAccountFromListParams, None]):
    """Remove an account from exactly one owned custom list, keeping it saved even after its
    last list. Repeating an absent membership succeeds.
    """

    operation_name = "nvRemoveAccountFromList"
    mapper = VoidWorkflowMapper[NvRemoveAccountFromListParams]("nv.removeAccountFromList")
