from __future__ import annotations

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams
from linkedapi.types.person import YearsOfExperience
from linkedapi.types.viewer_state import (
    ConnectionDegree,
    NvConnectionDegreeFilter,
    PersonViewerState,
)


class SearchPeopleFilter(LinkedApiModel):
    first_name: str | None = None
    last_name: str | None = None
    position: str | None = None
    locations: list[str] | None = None
    industries: list[str] | None = None
    current_companies: list[str] | None = None
    previous_companies: list[str] | None = None
    schools: list[str] | None = None
    connection_degrees: list[ConnectionDegree] | None = None


class SearchPeopleParams(BaseActionParams, LimitParams):
    term: str | None = None
    filter: SearchPeopleFilter | None = None
    custom_search_url: str | None = None


class SearchPeopleResult(LinkedApiModel):
    name: str | None = None
    urn: str | None = None
    public_url: str | None = None
    headline: str | None = None
    location: str | None = None
    avatar_url: str | None = None
    viewer_state: PersonViewerState | None = None


class NvSearchPeopleFilter(SearchPeopleFilter):
    years_of_experiences: list[YearsOfExperience] | None = None
    connection_degrees: list[NvConnectionDegreeFilter] | None = None  # type: ignore[assignment]


class NvSearchPeopleParams(BaseActionParams, LimitParams):
    term: str | None = None
    filter: NvSearchPeopleFilter | None = None
    custom_search_url: str | None = None


class NvSearchPeopleResult(LinkedApiModel):
    name: str | None = None
    urn: str | None = None
    hashed_url: str | None = None
    position: str | None = None
    location: str | None = None
    avatar_url: str | None = None
    viewer_state: PersonViewerState | None = None
