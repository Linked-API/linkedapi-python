from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from linkedapi import (
    LinkedApi,
    LinkedApiConfig,
    NvCreatedList,
    NvCreatedSavedSearch,
    NvCreateSavedSearchParams,
    NvDeleteSavedSearchParams,
    NvListAccount,
    NvListLead,
    NvRemoveAccountFromListParams,
    NvRemoveLeadFromListParams,
    NvRenameListParams,
    NvRetrieveAlertsParams,
    NvRetrieveListAccountsParams,
    NvRetrieveListLeadsParams,
    NvRetrieveSavedSearchesParams,
    NvSavedSearch,
)

LIST_ID = "7420000000000000001"
PERSON_URL = "https://www.linkedin.com/in/example-person"
COMPANY_URL = "https://www.linkedin.com/company/example-company"
SEARCH_URL = "https://www.linkedin.com/sales/search/people?query=example"


def client() -> LinkedApi:
    return LinkedApi(LinkedApiConfig(linked_api_token="test", identification_token="test"))


@pytest.mark.parametrize(
    "operation,action,params,expected",
    [
        (
            "nv_retrieve_list_leads",
            "nv.retrieveListLeads",
            NvRetrieveListLeadsParams(list_id=LIST_ID, limit=26),
            {"listId": LIST_ID, "limit": 26},
        ),
        (
            "nv_retrieve_list_accounts",
            "nv.retrieveListAccounts",
            NvRetrieveListAccountsParams(list_id=LIST_ID),
            {"listId": LIST_ID},
        ),
        (
            "nv_remove_lead_from_list",
            "nv.removeLeadFromList",
            NvRemoveLeadFromListParams(person_hashed_url=PERSON_URL, list_id=LIST_ID),
            {"personHashedUrl": PERSON_URL, "listId": LIST_ID},
        ),
        (
            "nv_remove_account_from_list",
            "nv.removeAccountFromList",
            NvRemoveAccountFromListParams(company_hashed_url=COMPANY_URL, list_id=LIST_ID),
            {"companyHashedUrl": COMPANY_URL, "listId": LIST_ID},
        ),
        (
            "nv_rename_list",
            "nv.renameList",
            NvRenameListParams(list_id=LIST_ID, name="  Prospects  "),
            {"listId": LIST_ID, "name": "Prospects"},
        ),
        (
            "nv_retrieve_saved_searches",
            "nv.retrieveSavedSearches",
            NvRetrieveSavedSearchesParams(type="lead"),
            {"type": "lead"},
        ),
        (
            "nv_create_saved_search",
            "nv.createSavedSearch",
            NvCreateSavedSearchParams(type="lead", custom_search_url=SEARCH_URL),
            {"type": "lead", "customSearchUrl": SEARCH_URL},
        ),
        (
            "nv_create_saved_search",
            "nv.createSavedSearch",
            NvCreateSavedSearchParams(
                type="lead", custom_search_url=SEARCH_URL, name="  Heads of Sales  "
            ),
            {"type": "lead", "customSearchUrl": SEARCH_URL, "name": "Heads of Sales"},
        ),
        (
            "nv_delete_saved_search",
            "nv.deleteSavedSearch",
            NvDeleteSavedSearchParams(saved_search_id=LIST_ID),
            {"savedSearchId": LIST_ID},
        ),
    ],
)
def test_root_requests(operation: str, action: str, params: Any, expected: dict[str, Any]) -> None:
    op = getattr(client(), operation)
    assert op.mapper.map_request(params) == {"actionType": action, **expected}
    if operation in {
        "nv_remove_lead_from_list",
        "nv_remove_account_from_list",
        "nv_delete_saved_search",
    }:
        assert op.mapper.map_response({"actionType": action, "success": True}).data is None


@pytest.mark.parametrize(
    "operation,action,model,row,is_array",
    [
        (
            "nv_rename_list",
            "nv.renameList",
            NvCreatedList,
            {
                "id": LIST_ID,
                "name": "Prospects",
                "type": "lead",
                "url": f"https://www.linkedin.com/sales/lists/people/{LIST_ID}",
            },
            False,
        ),
        (
            "nv_retrieve_list_leads",
            "nv.retrieveListLeads",
            NvListLead,
            {
                "name": "Example",
                "urn": "urn:li:member:123",
                "hashedUrl": PERSON_URL,
                "position": None,
                "companyName": None,
                "location": None,
                "addedToListAt": None,
            },
            True,
        ),
        (
            "nv_retrieve_list_accounts",
            "nv.retrieveListAccounts",
            NvListAccount,
            {
                "name": "Example",
                "urn": "urn:li:organization:123",
                "hashedUrl": COMPANY_URL,
                "industry": None,
                "employeesCount": None,
            },
            True,
        ),
        (
            "nv_retrieve_saved_searches",
            "nv.retrieveSavedSearches",
            NvSavedSearch,
            {
                "id": LIST_ID,
                "name": "Example",
                "type": "lead",
                "url": SEARCH_URL,
                "keywords": None,
                "createdAt": None,
                "lastViewedAt": None,
                "newResultsCount": None,
            },
            True,
        ),
        (
            "nv_create_saved_search",
            "nv.createSavedSearch",
            NvCreatedSavedSearch,
            {"id": LIST_ID, "name": "Example", "type": "lead", "url": SEARCH_URL},
            False,
        ),
    ],
)
def test_typed_results(
    operation: str, action: str, model: Any, row: dict[str, Any], is_array: bool
) -> None:
    result = getattr(client(), operation).mapper.map_response(
        {"actionType": action, "success": True, "data": [row] if is_array else row}
    )
    value = result.data[0] if is_array else result.data
    assert isinstance(value, model)
    assert value.model_dump(by_alias=True) == row
    assert result.errors == []


def test_alert_filter_fields_survive_pydantic_serialization() -> None:
    subjects = [
        "urn:li:fs_salesProfile:(ACwAAAExample,NAME_SEARCH,xyz)",
        "urn:li:fs_salesCompany:123",
    ]
    for filter_value in [
        {"list_id": LIST_ID, "subjects": subjects},
        {"listId": LIST_ID, "subjects": subjects},
    ]:
        params = NvRetrieveAlertsParams(filter=filter_value)
        assert client().nv_retrieve_alerts.mapper.map_request(params) == {
            "actionType": "nv.retrieveAlerts",
            "filter": {"listId": LIST_ID, "subjects": subjects},
        }


@pytest.mark.parametrize("name", ["", " ", "x" * 76, "one\ntwo"])
def test_rename_rejects_invalid_name(name: str) -> None:
    with pytest.raises(ValidationError):
        NvRenameListParams(list_id=LIST_ID, name=name)


@pytest.mark.parametrize("limit", [0, 1001])
def test_list_member_limits(limit: int) -> None:
    with pytest.raises(ValidationError):
        NvRetrieveListLeadsParams(list_id=LIST_ID, limit=limit)


@pytest.mark.parametrize(
    "operation,action,error_type",
    [
        ("nv_rename_list", "nv.renameList", "listNotRenamable"),
        ("nv_delete_saved_search", "nv.deleteSavedSearch", "savedSearchNotFound"),
    ],
)
def test_public_action_errors(operation: str, action: str, error_type: str) -> None:
    error = {"type": error_type, "message": "Fixture error"}
    result = getattr(client(), operation).mapper.map_response(
        {"actionType": action, "success": False, "error": error}
    )
    assert result.data is None
    assert [item.model_dump() for item in result.errors] == [error]


@pytest.mark.parametrize("name", ["", "   ", "a" * 257, "Heads\nof Sales"])
def test_create_saved_search_rejects_invalid_names(name: str) -> None:
    with pytest.raises(ValidationError):
        NvCreateSavedSearchParams(type="lead", custom_search_url=SEARCH_URL, name=name)
