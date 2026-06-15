from __future__ import annotations

from typing import Any

import requests

from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient
from linkedapi.types import LinkedApiResponse, serialize_value
from linkedapi.types.admin import AdminConfig


class AdminHttpClient(HttpClient[Any]):
    def __init__(
        self,
        config: AdminConfig,
        client: str | None = None,
        base_url: str = "https://api.linkedapi.io",
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.headers = {
            "Content-Type": "application/json",
            "linked-api-token": config.linked_api_token,
            "client": client or config.client,
        }

    def get(self, path: str) -> LinkedApiResponse[Any]:
        return self._request("GET", path)

    def post(self, path: str, data: Any | None = None) -> LinkedApiResponse[Any]:
        return self._request("POST", path, data)

    def delete(self, path: str) -> LinkedApiResponse[Any]:
        return self._request("DELETE", path)

    def _request(self, method: str, path: str, data: Any | None = None) -> LinkedApiResponse[Any]:
        try:
            response = self.session.request(
                method,
                f"{self.base_url}{path}",
                headers=self.headers,
                json=serialize_value(data) if data is not None else None,
            )
            return self._handle_response(response)
        except LinkedApiError:
            raise
        except requests.RequestException as error:
            raise LinkedApiError(
                "httpError", f"Request error: {error}", {"error": error}
            ) from error

    def _handle_response(self, response: requests.Response) -> LinkedApiResponse[Any]:
        if response.ok:
            return LinkedApiResponse[Any].model_validate(response.json())

        try:
            error_data = response.json()
            error = error_data["error"]
            raise LinkedApiError(error["type"], error["message"], error_data)
        except LinkedApiError:
            raise
        except (KeyError, TypeError, ValueError) as error:
            raise LinkedApiError(
                "httpError",
                f"HTTP {response.status_code}: {response.reason}",
                {
                    "status": response.status_code,
                    "statusText": response.reason,
                    "url": response.url,
                },
            ) from error
