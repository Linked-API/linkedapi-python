from __future__ import annotations

from pydantic import Field

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams


class NvRetrieveListLeadsParams(BaseActionParams):
    list_id: str = Field(min_length=1)
    limit: int | None = Field(default=None, ge=1, le=1000)


class NvRetrieveListAccountsParams(BaseActionParams):
    list_id: str = Field(min_length=1)
    limit: int | None = Field(default=None, ge=1, le=1000)


class NvRemoveLeadFromListParams(BaseActionParams):
    person_hashed_url: str = Field(min_length=1)
    list_id: str = Field(min_length=1)


class NvRemoveAccountFromListParams(BaseActionParams):
    company_hashed_url: str = Field(min_length=1)
    list_id: str = Field(min_length=1)


class NvListLead(LinkedApiModel):
    name: str
    urn: str
    hashed_url: str
    position: str | None
    company_name: str | None
    location: str | None
    added_to_list_at: str | None


class NvListAccount(LinkedApiModel):
    name: str
    urn: str
    hashed_url: str
    industry: str | None
    employees_count: int | None
