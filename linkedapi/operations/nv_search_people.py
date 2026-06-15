from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import NvSearchPeopleParams, NvSearchPeopleResult


class NvSearchPeople(Operation[NvSearchPeopleParams, list[NvSearchPeopleResult]]):
    """Search people on Sales Navigator."""

    operation_name = "nvSearchPeople"
    mapper = ArrayWorkflowMapper[NvSearchPeopleParams, NvSearchPeopleResult](
        "nv.searchPeople",
        NvSearchPeopleResult,
    )
