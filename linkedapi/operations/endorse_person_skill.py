from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import EndorsePersonSkillParams


class EndorsePersonSkill(Operation[EndorsePersonSkillParams, None]):
    """Endorse a first-degree connection's skill by its exact name."""

    operation_name = "endorsePersonSkill"
    mapper = VoidWorkflowMapper[EndorsePersonSkillParams]("st.endorsePersonSkill")
