from __future__ import annotations

from typing import Any

import pytest
import requests_mock
from pydantic import ValidationError

from linkedapi import (
    AdminConfig,
    AdminHttpClient,
    DeleteLimitsParams,
    GetLimitsParams,
    GetLimitsUsageParams,
    LinkedApiAdmin,
    SetLimitsParams,
)


@pytest.fixture
def admin() -> LinkedApiAdmin:
    return LinkedApiAdmin(
        AdminHttpClient(AdminConfig(linked_api_token="test-token"), base_url="https://api.test")
    )


@pytest.mark.parametrize("category", ["stEndorsements", "stSomethingNew"])
@pytest.mark.parametrize("method", ["get", "get_defaults", "get_usage"])
def test_limit_reads_accept_new_category_strings(
    admin: LinkedApiAdmin, requests_mock: requests_mock.Mocker, category: str, method: str
) -> None:
    entry: dict[str, Any] = {
        "category": category,
        "period": "daily",
        "maxValue": 50,
        "isEnabled": True,
    }
    if method == "get_usage":
        entry["currentValue"] = 12
        result_key = "usage"
        endpoint = "getUsage"
    else:
        result_key = "limits"
        endpoint = "getDefaults" if method == "get_defaults" else "get"
    requests_mock.post(
        f"https://api.test/admin/limits.{endpoint}",
        json={"success": True, "result": {result_key: [entry]}},
    )

    if method == "get":
        result = admin.limits.get(GetLimitsParams(account_id="test-account"))
        entries = result.limits
    elif method == "get_defaults":
        result = admin.limits.get_defaults()
        entries = result.limits
    else:
        usage_result = admin.limits.get_usage(GetLimitsUsageParams(account_id="test-account"))
        entries = usage_result.usage

    assert entries is not None
    assert len(entries) == 1
    assert entries[0].category == category
    assert entries[0].period == "daily"
    assert entries[0].max_value == 50
    assert entries[0].is_enabled is True


@pytest.mark.parametrize("method", ["set", "delete"])
def test_limit_writes_serialize_endorsements(
    admin: LinkedApiAdmin, requests_mock: requests_mock.Mocker, method: str
) -> None:
    requests_mock.post(f"https://api.test/admin/limits.{method}", json={"success": True})
    entry: dict[str, Any] = {"category": "stEndorsements", "period": "daily"}
    if method == "set":
        entry.update({"maxValue": 50, "isEnabled": True})
        params = SetLimitsParams.model_validate({"accountId": "test-account", "limits": [entry]})
        admin.limits.set(params)
    else:
        delete_params = DeleteLimitsParams.model_validate(
            {"accountId": "test-account", "limits": [entry]}
        )
        admin.limits.delete(delete_params)

    request = requests_mock.last_request
    assert request is not None
    assert request.json() == {"accountId": "test-account", "limits": [entry]}


@pytest.mark.parametrize("method", ["set", "delete"])
def test_limit_writes_reject_unknown_categories_before_http(
    admin: LinkedApiAdmin, requests_mock: requests_mock.Mocker, method: str
) -> None:
    entry: dict[str, Any] = {"category": "stSomethingNew", "period": "daily"}
    with pytest.raises(ValidationError) as error:
        if method == "set":
            entry["maxValue"] = 50
            admin.limits.set(
                SetLimitsParams.model_validate({"accountId": "test-account", "limits": [entry]})
            )
        else:
            admin.limits.delete(
                DeleteLimitsParams.model_validate({"accountId": "test-account", "limits": [entry]})
            )

    assert any(item["loc"] == ("limits", 0, "category") for item in error.value.errors())
    assert requests_mock.request_history == []
