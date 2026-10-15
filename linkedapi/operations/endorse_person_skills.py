from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import EndorsePersonSkillsMapper
from linkedapi.types import EndorsePersonSkillsParams, PersonSkillEndorsement


class EndorsePersonSkills(Operation[EndorsePersonSkillsParams, list[PersonSkillEndorsement]]):
    """Endorse selected skills and return each skill's outcome in profile order."""

    operation_name = "endorsePersonSkills"
    mapper = EndorsePersonSkillsMapper()
