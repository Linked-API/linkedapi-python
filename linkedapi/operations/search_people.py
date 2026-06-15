from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import SearchPeopleParams, SearchPeopleResult


class SearchPeople(Operation[SearchPeopleParams, list[SearchPeopleResult]]):
    """Search people on standard LinkedIn."""

    operation_name = "searchPeople"
    mapper = ArrayWorkflowMapper[SearchPeopleParams, SearchPeopleResult](
        "st.searchPeople",
        SearchPeopleResult,
    )
