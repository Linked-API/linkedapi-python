from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams

ConnectionStatus = Literal["connected", "pending", "notConnected"]


class ConnectionPerson(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    headline: str | None = None
    location: str | None = None
    profile_image_url: str | None = None


class SendConnectionRequestParams(BaseActionParams):
    person_url: str
    note: str | None = None
    email: str | None = None


class CheckConnectionStatusParams(BaseActionParams):
    person_url: str


class CheckConnectionStatusResult(LinkedApiModel):
    connection_status: ConnectionStatus | None = None


class WithdrawConnectionRequestParams(BaseActionParams):
    person_url: str
    unfollow: bool | None = None


class RetrievePendingRequestsResult(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    headline: str | None = None
    sent_time: str | None = None


class RetrieveConnectionsFilter(LinkedApiModel):
    first_name: str | None = None
    last_name: str | None = None
    position: str | None = None
    locations: list[str] | None = None
    industries: list[str] | None = None
    current_companies: list[str] | None = None
    previous_companies: list[str] | None = None
    schools: list[str] | None = None


class RetrieveConnectionsParams(LimitParams):
    since: str | None = None
    filter: RetrieveConnectionsFilter | None = None


class RetrieveConnectionsResult(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    headline: str | None = None
    location: str | None = None
    connected_at: str | None = None


class RemoveConnectionParams(BaseActionParams):
    person_url: str


class NvOpenPersonPageParams(BaseActionParams):
    person_hashed_url: str


class NvOpenPersonPageResult(LinkedApiModel):
    name: str | None = None
    public_url: str | None = None
    hashed_url: str | None = None
    headline: str | None = None
    location: str | None = None
    country_code: str | None = None
    position: str | None = None
    company_name: str | None = None
    company_hashed_url: str | None = None
