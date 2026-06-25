from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel

AdminAccountStatus = Literal["active", "frozen", "reconnection_required"]
ConnectionSessionStatus = Literal[
    "pending",
    "preparing",
    "serving",
    "streaming",
    "success",
    "expired",
    "error",
    "cancelled",
]


class AdminAccount(LinkedApiModel):
    id: str | None = None
    name: str | None = None
    url: str | None = None
    avatar_url: str | None = None
    headline: str | None = None
    country_code: str | None = None
    identification_token: str | None = None
    status: AdminAccountStatus | None = None
    connected_at: str | None = None
    reconnection_session_id: str | None = None
    reconnection_link: str | None = None


class PendingConnectionSession(LinkedApiModel):
    session_id: str | None = None
    status: str | None = None


class AccountsResult(LinkedApiModel):
    accounts: list[AdminAccount] | None = None
    pending_connection_sessions: list[PendingConnectionSession] | None = None


class DisconnectParams(LinkedApiModel):
    account_id: str


class ReparseAccountInfoParams(LinkedApiModel):
    account_id: str


class ReparseAccountInfoResult(LinkedApiModel):
    workflow_id: str | None = None


class RegenerateTokenParams(LinkedApiModel):
    account_id: str


class RegenerateTokenResult(LinkedApiModel):
    token: str | None = None


class CreateConnectionSessionResult(LinkedApiModel):
    session_id: str | None = None
    connection_link: str | None = None


class CreateReconnectionSessionParams(LinkedApiModel):
    account_id: str


class CreateReconnectionSessionResult(LinkedApiModel):
    reconnection_session_id: str | None = None
    reconnection_link: str | None = None


class GetConnectionSessionParams(LinkedApiModel):
    session_id: str


class ConnectionSession(LinkedApiModel):
    session_id: str | None = None
    status: ConnectionSessionStatus | None = None
    type: str | None = None


class ConnectionSessionResult(LinkedApiModel):
    session: ConnectionSession | None = None


class CancelConnectionSessionParams(LinkedApiModel):
    session_id: str
