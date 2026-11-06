from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import NvListAccount, NvRetrieveListAccountsParams


class NvRetrieveListAccounts(Operation[NvRetrieveListAccountsParams, list[NvListAccount]]):
    """Retrieve list accounts from an owned Sales Navigator list."""

    operation_name = "nvRetrieveListAccounts"
    mapper = ArrayWorkflowMapper[NvRetrieveListAccountsParams, NvListAccount](
        "nv.retrieveListAccounts", NvListAccount
    )
