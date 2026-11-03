from __future__ import annotations

from typing import Any

import pytest
import requests_mock
from pydantic import ValidationError

from linkedapi import (
    LinkedApi,
    LinkedApiConfig,
    NvAlert,
    NvRetrieveAlertsFilter,
    NvRetrieveAlertsParams,
)

ALERT = {
    "id": "urn:li:notification:123",
    "type": "FUTURE_MACHINE_TYPE",
    "publishedAt": "2026-10-01T00:00:00.000Z",
    "subject": {
        "type": "lead",
        "urn": "urn:li:fs_salesProfile:123",
        "name": None,
        "url": "https://www.linkedin.com/sales/lead/123",
        "saved": None,
    },
    "headline": None,
    "text": None,
    "subline": None,
    "url": None,
    "relatedEntityUrn": None,
}


@pytest.mark.parametrize(
    "params, expected",
    [
        (NvRetrieveAlertsParams(), {}),
        (
            NvRetrieveAlertsParams(
                limit=1000,
                sort="relevance",
                filter=NvRetrieveAlertsFilter(
                    category="account",
                    types=["FUTURE_MACHINE_TYPE"],
                    since="2026-10-01T00:00:00Z",
                    exclude_suggested=True,
                ),
            ),
            {
                "limit": 1000,
                "sort": "relevance",
                "filter": {
                    "category": "account",
                    "types": ["FUTURE_MACHINE_TYPE"],
                    "since": "2026-10-01T00:00:00Z",
                    "excludeSuggested": True,
                },
            },
        ),
        (
            NvRetrieveAlertsParams(
                filter=NvRetrieveAlertsFilter(types=[], exclude_suggested=False)
            ),
            {"filter": {"types": [], "excludeSuggested": False}},
        ),
    ],
)
def test_alerts_root_mapping_and_nullable_result(
    requests_mock: requests_mock.Mocker,
    params: NvRetrieveAlertsParams,
    expected: dict[str, Any],
) -> None:
    client = LinkedApi(
        LinkedApiConfig(
            linked_api_token="test", identification_token="test", base_url="https://api.test"
        )
    )
    requests_mock.post(
        "https://api.test/workflows",
        json={"success": True, "result": {"workflowId": "alerts", "workflowStatus": "pending"}},
    )
    requests_mock.get(
        "https://api.test/workflows/alerts",
        json={
            "success": True,
            "result": {
                "workflowStatus": "completed",
                "completion": {"actionType": "nv.retrieveAlerts", "success": True, "data": [ALERT]},
            },
        },
    )
    operation = client.nv_retrieve_alerts
    assert operation in client.operations
    workflow = operation.execute(params)
    result = operation.result(workflow.workflow_id)
    assert requests_mock.request_history[0].json() == {
        "actionType": "nv.retrieveAlerts",
        **expected,
    }
    assert result.errors == []
    assert result.data is not None
    assert isinstance(result.data[0], NvAlert)
    assert result.data[0].model_dump(by_alias=True) == ALERT


@pytest.mark.parametrize("limit", [0, 1001])
def test_alerts_limit_bounds(limit: int) -> None:
    with pytest.raises(ValidationError):
        NvRetrieveAlertsParams(limit=limit)


@pytest.mark.parametrize(
    "completion, expected_data, expected_errors",
    [
        ({"success": True, "data": []}, [], []),
        (
            {"success": False, "error": {"type": "unexpectedError", "message": "Capture failed"}},
            None,
            [{"type": "unexpectedError", "message": "Capture failed"}],
        ),
    ],
)
def test_empty_alerts_and_failures_remain_distinct(
    completion: dict[str, Any],
    expected_data: list[Any] | None,
    expected_errors: list[dict[str, str]],
) -> None:
    mapper = LinkedApi(
        LinkedApiConfig(linked_api_token="test", identification_token="test")
    ).nv_retrieve_alerts.mapper
    result = mapper.map_response({"actionType": "nv.retrieveAlerts", **completion})
    assert result.data == expected_data
    assert [error.model_dump() for error in result.errors] == expected_errors
