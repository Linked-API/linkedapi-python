from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import AcceptInvitationParams


class AcceptInvitation(Operation[AcceptInvitationParams, None]):
    """Accept an incoming standard LinkedIn invitation."""

    operation_name = "acceptInvitation"
    mapper = VoidWorkflowMapper[AcceptInvitationParams]("st.acceptInvitation")
