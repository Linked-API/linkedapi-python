from __future__ import annotations

from typing import Any

import pytest
import requests_mock
from pydantic import ValidationError

from linkedapi import (
    LINKED_API_ACTION_ERROR_TYPES,
    LinkedApi,
    LinkedApiConfig,
    NvCreatedList,
    NvCreateListParams,
    NvDeleteListParams,
)

LIST_ID = "7420000000000000001"


def client() -> LinkedApi:
    return LinkedApi(
        LinkedApiConfig(
            linked_api_token="test", identification_token="test", base_url="https://api.test"
        )
    )


def queue_workflow(mock: requests_mock.Mocker, completion: dict[str, Any]) -> None:
    mock.post(
        "https://api.test/workflows",
        json={"success": True, "result": {"workflowId": "list", "workflowStatus": "pending"}},
    )
    mock.get(
        "https://api.test/workflows/list",
        json={"success": True, "result": {"workflowStatus": "completed", "completion": completion}},
    )


@pytest.mark.parametrize("list_type,description", [("lead", None), ("account", "  Europe  ")])
def test_create_root_request_and_created_list(
    requests_mock: requests_mock.Mocker, list_type: str, description: str | None
) -> None:
    sdk = client()
    list_path = "people" if list_type == "lead" else "accounts"
    row = {
        "id": LIST_ID,
        "name": "Prospects",
        "type": list_type,
        "url": f"https://www.linkedin.com/sales/lists/{list_path}/{LIST_ID}",
    }
    params = NvCreateListParams.model_validate(
        {"type": list_type, "name": "  Prospects  ", "description": description}
    )
    queue_workflow(requests_mock, {"actionType": "nv.createList", "success": True, "data": row})
    assert sdk.nv_create_list in sdk.operations
    assert sdk.nv_create_list.operation_name == "nvCreateList"
    started = sdk.nv_create_list.execute(params)
    result = sdk.nv_create_list.result(started.workflow_id)
    expected = {"actionType": "nv.createList", "type": list_type, "name": "Prospects"}
    if description is not None:
        expected["description"] = description
    assert requests_mock.request_history[0].json() == expected
    assert isinstance(result.data, NvCreatedList)
    assert result.data.model_dump(by_alias=True) == row
    assert result.errors == []


def test_delete_exact_string_id_and_void_result(requests_mock: requests_mock.Mocker) -> None:
    sdk = client()
    queue_workflow(requests_mock, {"actionType": "nv.deleteList", "success": True})
    assert sdk.nv_delete_list in sdk.operations
    assert sdk.nv_delete_list.operation_name == "nvDeleteList"
    started = sdk.nv_delete_list.execute(NvDeleteListParams(list_id=LIST_ID))
    result = sdk.nv_delete_list.result(started.workflow_id)
    assert requests_mock.request_history[0].json() == {
        "actionType": "nv.deleteList",
        "listId": LIST_ID,
    }
    assert result.data is None
    assert result.errors == []


@pytest.mark.parametrize(
    "operation,action,error_type",
    [
        ("nv_create_list", "nv.createList", error)
        for error in [
            "listAlreadyExists",
            "interfaceLanguageNotSupported",
            "noSalesNavigator",
            "unexpectedError",
        ]
    ]
    + [
        ("nv_delete_list", "nv.deleteList", error)
        for error in [
            "listNotFound",
            "listNotDeletable",
            "interfaceLanguageNotSupported",
            "noSalesNavigator",
            "unexpectedError",
        ]
    ],
)
def test_action_errors_preserved(
    requests_mock: requests_mock.Mocker, operation: str, action: str, error_type: str
) -> None:
    sdk = client()
    error = {"type": error_type, "message": "Fixture error"}
    queue_workflow(requests_mock, {"actionType": action, "success": False, "error": error})
    op = getattr(sdk, operation)
    params = (
        NvCreateListParams(type="lead", name="Prospects")
        if operation == "nv_create_list"
        else NvDeleteListParams(list_id=LIST_ID)
    )
    started = op.execute(params)
    result = op.result(started.workflow_id)
    assert result.data is None
    assert [item.model_dump() for item in result.errors] == [error]
    assert error_type in LINKED_API_ACTION_ERROR_TYPES


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"type": "other", "name": "Prospects"},
        {"type": "lead"},
        {"type": "lead", "name": " "},
        {"type": "lead", "name": "x" * 76},
        {"type": "lead", "name": "Prospects", "description": "x" * 351},
    ],
)
def test_create_rejects_invalid_params(params: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        NvCreateListParams.model_validate(params)


def test_create_limits_apply_after_name_trim_and_description_is_preserved() -> None:
    params = NvCreateListParams(type="account", name=" " + "x" * 75 + " ", description=" " * 350)
    assert params.name == "x" * 75
    assert params.description == " " * 350


@pytest.mark.parametrize("list_id", [7420000000000000001, "", None])
def test_delete_rejects_non_string_or_empty_id(list_id: Any) -> None:
    with pytest.raises(ValidationError):
        NvDeleteListParams.model_validate({"listId": list_id})
