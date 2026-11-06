from __future__ import annotations

from typing import Literal

from pydantic import Field

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams


class NvSaveLeadParams(BaseActionParams):
    person_hashed_url: str
    list_id: str | None = Field(default=None, min_length=1)


class NvUnsaveLeadParams(BaseActionParams):
    person_hashed_url: str


class NvSaveAccountParams(BaseActionParams):
    company_hashed_url: str
    list_id: str | None = Field(default=None, min_length=1)


class NvUnsaveAccountParams(BaseActionParams):
    company_hashed_url: str


class NvRetrieveListsParams(BaseActionParams):
    type: Literal["lead", "account"]


class NvList(LinkedApiModel):
    id: str
    name: str
    type: Literal["lead", "account"] | str
    source: str
    entity_count: int | None
    url: str
