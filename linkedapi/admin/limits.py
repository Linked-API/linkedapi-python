from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient
from linkedapi.types.admin import (
    DeleteLimitsParams,
    GetLimitsParams,
    GetLimitsUsageParams,
    LimitsResult,
    LimitUsageResult,
    ResetLimitsParams,
    SetLimitsParams,
)

TModel = TypeVar("TModel", bound=BaseModel)


class AdminLimits:
    def __init__(self, http_client: HttpClient[Any]) -> None:
        self.http_client = http_client

    def get_defaults(self) -> LimitsResult:
        return self._post_result(
            "/admin/limits.getDefaults", LimitsResult, "Failed to get default limits"
        )

    def get(self, params: GetLimitsParams) -> LimitsResult:
        return self._post_result("/admin/limits.get", LimitsResult, "Failed to get limits", params)

    def get_usage(self, params: GetLimitsUsageParams) -> LimitUsageResult:
        return self._post_result(
            "/admin/limits.getUsage", LimitUsageResult, "Failed to get limits usage", params
        )

    def set(self, params: SetLimitsParams) -> None:
        self._post_void("/admin/limits.set", "Failed to set limits", params)

    def delete(self, params: DeleteLimitsParams) -> None:
        self._post_void("/admin/limits.delete", "Failed to delete limits", params)

    def reset_to_defaults(self, params: ResetLimitsParams) -> None:
        self._post_void("/admin/limits.resetToDefaults", "Failed to reset limits", params)

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
