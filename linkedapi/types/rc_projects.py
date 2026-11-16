from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, StringConstraints, field_validator

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams
from linkedapi.types.rc_people import RcSearchPeopleResult

RcProjectStage = Literal["uncontacted", "contacted", "replied", "archived"]


class RcRetrieveProjectsParams(BaseActionParams):
    limit: int | None = Field(default=None, ge=1, le=1000)


class RcRetrieveProjectCandidatesParams(RcRetrieveProjectsParams):
    project_id: str = Field(pattern=r"^\d+$")
    stage: RcProjectStage | None = None


class RcSaveToProjectParams(BaseActionParams):
    project_id: str = Field(pattern=r"^\d+$")
    person_url: str


class RcCreateProjectParams(BaseActionParams):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]

    @field_validator("name", mode="before")
    @classmethod
    def _validate_single_line_name(cls, value: str) -> str:
        if isinstance(value, str) and ("\r" in value or "\n" in value):
            raise ValueError("Project name must be a single line")
        return value


class RcRenameProjectParams(RcCreateProjectParams):
    project_id: str = Field(pattern=r"^\d+$")
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("description", mode="before")
    @classmethod
    def _normalize_description(cls, value: str | None) -> str | None:
        return value.replace("\r\n", "\n").replace("\r", "\n") if isinstance(value, str) else value


class RcArchiveProjectParams(BaseActionParams):
    project_id: str = Field(pattern=r"^\d+$")


class RcProject(LinkedApiModel):
    project_id: str
    name: str
    created_at: str
    candidate_count: int
    project_url: str


class RcProjectCandidate(RcSearchPeopleResult):
    stage: RcProjectStage | str


class RcCreatedProject(LinkedApiModel):
    project_id: str
    project_url: str
    name: str | None


class RcSaveToProjectResult(LinkedApiModel):
    already_in_project: bool


class RcArchiveProjectResult(LinkedApiModel):
    already_archived: bool
