from __future__ import annotations

from datetime import date, datetime

import requests

from linkedapi.errors import LinkedApiError
from linkedapi.types.changelog import ChangelogResponse


def get_changelog(
    since: str | date | datetime | None = None,
    *,
    url: str = "https://linkedapi.io/api/changelog",
) -> ChangelogResponse:
    """Read the public Linked API changelog.

    A release counts as shipped at the end of its week, so callers deduplicate by date.

    Raises:
        LinkedApiError: on a non-2xx response or network failure.
    """
    since_value = since.isoformat() if isinstance(since, date) else since
    try:
        response = requests.get(
            url, params={"since": since_value} if since_value is not None else None
        )
    except requests.RequestException as error:
        raise LinkedApiError("httpError", f"Request error: {error}", {"error": error}) from error

    if not 200 <= response.status_code < 300:
        try:
            error_data = response.json()
        except ValueError:
            error_data = None
        message = f"HTTP {response.status_code}: {response.reason}"
        if isinstance(error_data, dict) and isinstance(error_data.get("error"), str):
            message = error_data["error"]
        raise LinkedApiError(
            "httpError",
            message,
            {"status": response.status_code, "statusText": response.reason, "url": response.url},
        )

    return ChangelogResponse.model_validate(response.json())
