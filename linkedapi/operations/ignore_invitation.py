from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import IgnoreInvitationParams


class IgnoreInvitation(Operation[IgnoreInvitationParams, None]):
    """Ignore an incoming standard LinkedIn invitation."""

    operation_name = "ignoreInvitation"
    mapper = VoidWorkflowMapper[IgnoreInvitationParams]("st.ignoreInvitation")
