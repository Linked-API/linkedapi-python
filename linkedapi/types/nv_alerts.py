from __future__ import annotations

from typing import Literal

from pydantic import Field

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams


class NvRetrieveAlertsFilter(LinkedApiModel):
    category: Literal["lead", "account"] | None = None
    types: list[str] | None = None
    since: str | None = None
    exclude_suggested: bool | None = None


class NvRetrieveAlertsParams(BaseActionParams):
    limit: int | None = Field(default=None, ge=1, le=1000)
    sort: Literal["latest", "relevance"] | None = None
    filter: NvRetrieveAlertsFilter | None = None


class NvAlertSubject(LinkedApiModel):
    type: Literal["lead", "account"] | str
    urn: str
    name: str | None
    url: str
    saved: bool | None


class NvAlert(LinkedApiModel):
    id: str
    type: str
    published_at: str
    subject: NvAlertSubject
    headline: str | None
    text: str | None
    subline: str | None
    url: str | None
    related_entity_urn: str | None
