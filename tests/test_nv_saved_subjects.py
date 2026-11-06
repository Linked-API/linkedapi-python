from __future__ import annotations

from typing import Any

import pytest
import requests_mock
from pydantic import ValidationError

from linkedapi import (
    LINKED_API_ACTION_ERROR_TYPES,
    LinkedApi,
    LinkedApiConfig,
    NvList,
    NvRetrieveListsParams,
    NvSaveAccountParams,
    NvSaveLeadParams,
    NvUnsaveAccountParams,
    NvUnsaveLeadParams,
)

PERSON_URL = "https://www.linkedin.com/sales/lead/example"
COMPANY_URL = "https://www.linkedin.com/sales/company/123"
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
        json={"success": True, "result": {"workflowId": "saved", "workflowStatus": "pending"}},
    )
    mock.get(
        "https://api.test/workflows/saved",
        json={"success": True, "result": {"workflowStatus": "completed", "completion": completion}},
    )


@pytest.mark.parametrize(
    "name,action_type,params,expected",
    [
        (
            "nv_save_lead",
            "nv.saveLead",
            NvSaveLeadParams(person_hashed_url=PERSON_URL),
            {"personHashedUrl": PERSON_URL},
        ),
        (
            "nv_save_lead",
            "nv.saveLead",
            NvSaveLeadParams(person_hashed_url=PERSON_URL, list_id=LIST_ID),
            {"personHashedUrl": PERSON_URL, "listId": LIST_ID},
        ),
        (
            "nv_unsave_lead",
            "nv.unsaveLead",
            NvUnsaveLeadParams(person_hashed_url=PERSON_URL),
            {"personHashedUrl": PERSON_URL},
        ),
        (
            "nv_save_account",
            "nv.saveAccount",
            NvSaveAccountParams(company_hashed_url=COMPANY_URL),
            {"companyHashedUrl": COMPANY_URL},
        ),
        (
            "nv_save_account",
            "nv.saveAccount",
            NvSaveAccountParams(company_hashed_url=COMPANY_URL, list_id=LIST_ID),
            {"companyHashedUrl": COMPANY_URL, "listId": LIST_ID},
        ),
        (
            "nv_unsave_account",
            "nv.unsaveAccount",
            NvUnsaveAccountParams(company_hashed_url=COMPANY_URL),
            {"companyHashedUrl": COMPANY_URL},
        ),
    ],
)
def test_mutation_root_contract(
    requests_mock: requests_mock.Mocker,
    name: str,
    action_type: str,
    params: Any,
    expected: dict[str, Any],
) -> None:
    sdk = client()
    operation = getattr(sdk, name)
    assert operation in sdk.operations
    queue_workflow(requests_mock, {"actionType": action_type, "success": True})
    workflow = operation.execute(params)
    result = operation.result(workflow.workflow_id)
    assert requests_mock.request_history[0].json() == {"actionType": action_type, **expected}
    assert result.data is None
    assert result.errors == []


@pytest.mark.parametrize(
    "error_type",
    ["listNotFound", "personNotFound", "companyNotFound", "noSalesNavigator", "unexpectedError"],
)
def test_mutation_preserves_action_errors(
    requests_mock: requests_mock.Mocker, error_type: str
) -> None:
    sdk = client()
    error = {"type": error_type, "message": "Fixture error"}
    queue_workflow(requests_mock, {"actionType": "nv.saveLead", "success": False, "error": error})
    workflow = sdk.nv_save_lead.execute(
        NvSaveLeadParams(person_hashed_url=PERSON_URL, list_id=LIST_ID)
    )
    result = sdk.nv_save_lead.result(workflow.workflow_id)
    assert result.data is None
    assert [item.model_dump() for item in result.errors] == [error]
    assert "listNotFound" in LINKED_API_ACTION_ERROR_TYPES


@pytest.mark.parametrize("list_type", ["lead", "account"])
def test_list_contract_preserves_string_id_source_and_null_count(
    requests_mock: requests_mock.Mocker, list_type: str
) -> None:
    sdk = client()
    row = {
        "id": LIST_ID,
        "name": "Prospects",
        "type": list_type,
        "source": "FUTURE_SOURCE",
        "entityCount": None,
        "url": f"https://www.linkedin.com/sales/lists/{list_type}/{LIST_ID}",
    }
    queue_workflow(
        requests_mock, {"actionType": "nv.retrieveLists", "success": True, "data": [row]}
    )
    workflow = sdk.nv_retrieve_lists.execute(
        NvRetrieveListsParams.model_validate({"type": list_type})
    )
    result = sdk.nv_retrieve_lists.result(workflow.workflow_id)
    assert sdk.nv_retrieve_lists in sdk.operations
    assert requests_mock.request_history[0].json() == {
        "actionType": "nv.retrieveLists",
        "type": list_type,
    }
    assert result.errors == []
    assert result.data is not None
    assert isinstance(result.data[0], NvList)
    assert result.data[0].model_dump(by_alias=True) == row


@pytest.mark.parametrize(
    "completion,expected_data,expected_errors",
    [
        ({"success": True, "data": []}, [], []),
        (
            {"success": False, "error": {"type": "noSalesNavigator", "message": "Fixture error"}},
            None,
            [{"type": "noSalesNavigator", "message": "Fixture error"}],
        ),
    ],
)
def test_empty_catalog_and_failure_are_distinct(
    completion: dict[str, Any], expected_data: Any, expected_errors: list[dict[str, str]]
) -> None:
    result = client().nv_retrieve_lists.mapper.map_response(
        {"actionType": "nv.retrieveLists", **completion}
    )
    assert result.data == expected_data
    assert [item.model_dump() for item in result.errors] == expected_errors


@pytest.mark.parametrize("params", [{}, {"type": "other"}])
def test_list_type_is_required_and_closed(params: dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        NvRetrieveListsParams.model_validate(params)


@pytest.mark.parametrize("list_id", [7420000000000000001, ""])
def test_save_list_id_rejects_numbers_and_empty_strings(list_id: Any) -> None:
    with pytest.raises(ValidationError):
        NvSaveLeadParams(person_hashed_url=PERSON_URL, list_id=list_id)
    with pytest.raises(ValidationError):
        NvSaveAccountParams(company_hashed_url=COMPANY_URL, list_id=list_id)
