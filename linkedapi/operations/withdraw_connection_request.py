from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import WithdrawConnectionRequestParams


class WithdrawConnectionRequest(Operation[WithdrawConnectionRequestParams, None]):
    """Withdraw a pending standard LinkedIn connection request."""

    operation_name = "withdrawConnectionRequest"
    mapper = VoidWorkflowMapper[WithdrawConnectionRequestParams]("st.withdrawConnectionRequest")
