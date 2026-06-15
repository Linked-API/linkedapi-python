from __future__ import annotations

from typing import Any

import pytest

from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient
from linkedapi.types import LinkedApiRequestError, LinkedApiResponse


class FakeHttpClient(HttpClient[Any]):
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, Any | None]] = []
        self.responses: list[LinkedApiResponse[Any] | LinkedApiError] = []

    def queue_response(
        self,
        *,
        success: bool = True,
        result: Any | None = None,
        error: LinkedApiRequestError | None = None,
    ) -> None:
        self.responses.append(LinkedApiResponse[Any](success=success, result=result, error=error))

    def queue_error(self, error: LinkedApiError) -> None:
        self.responses.append(error)

    def get(self, path: str) -> LinkedApiResponse[Any]:
        self.calls.append(("GET", path, None))
        return self._next()

    def post(self, path: str, data: Any | None = None) -> LinkedApiResponse[Any]:
        self.calls.append(("POST", path, data))
        return self._next()

    def delete(self, path: str) -> LinkedApiResponse[Any]:
        self.calls.append(("DELETE", path, None))
        return self._next()

    def _next(self) -> LinkedApiResponse[Any]:
        value = self.responses.pop(0)
        if isinstance(value, LinkedApiError):
            raise value
        return value


@pytest.fixture
def fake_http_client() -> FakeHttpClient:
    return FakeHttpClient()


@pytest.fixture
def person_data() -> dict[str, Any]:
    return {
        "name": "Jane Doe",
        "publicUrl": "https://www.linkedin.com/in/jane-doe",
        "hashedUrl": "hash",
        "headline": "Founder",
        "location": "New York",
        "countryCode": "us",
        "position": "CEO",
        "companyName": "Acme",
        "companyHashedUrl": "company-hash",
        "followersCount": 100,
        "about": None,
    }
