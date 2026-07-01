from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient
from linkedapi.types.admin import (
    AccountsResult,
    CancelConnectionSessionParams,
    ConnectionSessionResult,
    CreateConnectionSessionResult,
    CreateReconnectionSessionParams,
    CreateReconnectionSessionResult,
    DisconnectParams,
    GetConnectionSessionParams,
    RegenerateTokenParams,
    RegenerateTokenResult,
    ReparseAccountInfoParams,
    ReparseAccountInfoResult,
)

TModel = TypeVar("TModel", bound=BaseModel)


class AdminAccounts:
    def __init__(self, http_client: HttpClient[Any]) -> None:
        self.http_client = http_client

    def get_all(self) -> AccountsResult:
        return self._post_result("/admin/accounts.getAll", AccountsResult, "Failed to get accounts")

    def disconnect(self, params: DisconnectParams) -> None:
        self._post_void("/admin/accounts.disconnect", "Failed to disconnect account", params)

    def reparse_account_info(self, params: ReparseAccountInfoParams) -> ReparseAccountInfoResult:
        return self._post_result(
            "/admin/accounts.reparseAccountInfo",
            ReparseAccountInfoResult,
            "Failed to reparse account info",
            params,
        )

    def regenerate_identification_token(
        self,
        params: RegenerateTokenParams,
    ) -> RegenerateTokenResult:
        return self._post_result(
            "/admin/accounts.regenerateIdentificationToken",
            RegenerateTokenResult,
            "Failed to regenerate token",
            params,
        )

    def create_connection_session(self) -> CreateConnectionSessionResult:
        return self._post_result(
            "/admin/accounts.createConnectionSession",
            CreateConnectionSessionResult,
            "Failed to create connection session",
        )

    def create_reconnection_session(
        self,
        params: CreateReconnectionSessionParams,
    ) -> CreateReconnectionSessionResult:
        return self._post_result(
            "/admin/accounts.createReconnectionSession",
            CreateReconnectionSessionResult,
            "Failed to create reconnection session",
            params,
        )

    def get_connection_session(
        self,
        params: GetConnectionSessionParams,
    ) -> ConnectionSessionResult:
        return self._post_result(
            "/admin/accounts.getConnectionSession",
            ConnectionSessionResult,
            "Failed to get connection session",
            params,
        )

    def cancel_connection_session(self, params: CancelConnectionSessionParams) -> None:
        self._post_void(
            "/admin/accounts.cancelConnectionSession",
            "Failed to cancel connection session",
            params,
        )

    def _post_result(
        self,
        path: str,
        model: type[TModel],
        default_message: str,
        params: Any | None = None,
    ) -> TModel:
        response = self.http_client.post(path, params)
        if response.success and response.result is not None:
            return model.model_validate(response.result)
        raise LinkedApiError(
            response.error.type if response.error else "httpError",
            response.error.message if response.error else default_message,
        )

    def _post_void(self, path: str, default_message: str, params: Any | None = None) -> None:
        response = self.http_client.post(path, params)
        if response.success:
            return
        raise LinkedApiError(
            response.error.type if response.error else "httpError",
            response.error.message if response.error else default_message,
        )
