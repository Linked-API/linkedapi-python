from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest
import requests
import requests_mock

from linkedapi import (
    ChangelogItem,
    ChangelogRelease,
    ChangelogResponse,
    LinkedApiError,
    get_changelog,
)

URL = "https://linkedapi.io/api/changelog"
CHANGELOG: dict[str, Any] = {
    "since": None,
    "count": 1,
    "entries": [
        {
            "date": "2026-10-05",
            "items": [
                {
                    "title": "Webhook signing",
                    "body": "Verify signed deliveries.",
                    "docs": "/docs/webhooks",
                },
            ],
        }
    ],
}


def test_public_changelog_models_and_no_token(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get(URL, json=CHANGELOG)
    result = get_changelog()
    assert isinstance(result, ChangelogResponse)
    assert isinstance(result.entries[0], ChangelogRelease)
    assert isinstance(result.entries[0].items[0], ChangelogItem)
    assert result.model_dump(by_alias=True) == CHANGELOG
    request = requests_mock.last_request
    assert request is not None
    assert request.method == "GET"
    assert request.url == URL
    for header in ["linked-api-token", "identification-token", "Authorization"]:
        assert header not in request.headers


@pytest.mark.parametrize(
    ("since", "expected"),
    [
        ("2026-10-01", "2026-10-01"),
        ("2026-10-01T12:34:56+02:00", "2026-10-01T12:34:56+02:00"),
        (date(2026, 10, 1), "2026-10-01"),
        (
            datetime(2026, 10, 1, 12, 34, 56, tzinfo=timezone(timedelta(hours=2))),
            "2026-10-01T12:34:56+02:00",
        ),
    ],
)
def test_since_building(
    requests_mock: requests_mock.Mocker, since: str | date | datetime, expected: str
) -> None:
    payload = CHANGELOG | {"since": expected}
    requests_mock.get(URL, json=payload)
    result = get_changelog(since)
    request = requests_mock.last_request
    assert request is not None
    assert parse_qs(urlsplit(request.url).query) == {"since": [expected]}
    if "+" in expected:
        assert "%2B" in request.url
    assert result.model_dump() == payload


def test_endpoint_override(requests_mock: requests_mock.Mocker) -> None:
    url = "http://127.0.0.1:3000/api/changelog?source=sdk"
    requests_mock.get(url, json=CHANGELOG)
    get_changelog("2026-10-01", url=url)
    request = requests_mock.last_request
    assert request is not None
    assert request.url.startswith(url + "&")
    assert parse_qs(urlsplit(request.url).query) == {"source": ["sdk"], "since": ["2026-10-01"]}


@pytest.mark.parametrize("status", [400, 500])
def test_server_error_message(requests_mock: requests_mock.Mocker, status: int) -> None:
    requests_mock.get(URL, status_code=status, json={"error": "Server explanation"})
    with pytest.raises(LinkedApiError) as error:
        get_changelog("invalid")
    assert error.value.type == "httpError"
    assert error.value.message == "Server explanation"


def test_naive_datetime_is_explained_by_server(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get(URL, status_code=400, json={"error": "since requires a time zone"})
    with pytest.raises(LinkedApiError, match="since requires a time zone"):
        get_changelog(datetime(2026, 10, 1, 12, 34, 56))
    request = requests_mock.last_request
    assert request is not None
    assert parse_qs(urlsplit(request.url).query) == {"since": ["2026-10-01T12:34:56"]}


def test_http_status_fallback(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get(URL, status_code=502, text="Bad Gateway")
    with pytest.raises(LinkedApiError) as error:
        get_changelog()
    assert error.value.type == "httpError"
    assert error.value.message.startswith("HTTP 502:")


def test_network_failure(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get(URL, exc=requests.exceptions.ConnectTimeout("offline"))
    with pytest.raises(LinkedApiError) as error:
        get_changelog()
    assert error.value.type == "httpError"
    assert error.value.message == "Request error: offline"
