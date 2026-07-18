from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import Invitation


class RetrieveInvitations(Operation[None, list[Invitation]]):
    """Retrieve incoming LinkedIn invitations."""

    operation_name = "retrieveInvitations"
    mapper = ArrayWorkflowMapper[None, Invitation](
        "st.retrieveInvitations",
        Invitation,
    )
