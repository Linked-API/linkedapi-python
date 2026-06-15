from __future__ import annotations

import pytest
import requests
import requests_mock

from linkedapi import FetchPersonParams, LinkedApiConfig, LinkedApiError, LinkedApiHttpClient


def test_post_sends_auth_headers_and_camel_case_json(
    requests_mock: requests_mock.Mocker,
) -> None:
    requests_mock.post(
        "https://api.test/workflows",
        json={"success": True, "result": {"workflowId": "wf1", "workflowStatus": "pending"}},
    )
    client = LinkedApiHttpClient(
        LinkedApiConfig(
            linked_api_token="lat",
            identification_token="idt",
            base_url="https://api.test",
        )
    )

    response = client.post(
        "/workflows",
        FetchPersonParams(person_url="u", retrieve_experience=True),
    )

    request = requests_mock.last_request
    assert response.success is True
    assert response.result == {"workflowId": "wf1", "workflowStatus": "pending"}
    assert request is not None
    assert request.method == "POST"
    assert request.url == "https://api.test/workflows"
    assert request.headers["linked-api-token"] == "lat"
    assert request.headers["identification-token"] == "idt"
    assert request.headers["client"] == "python"
    assert request.headers["Content-Type"] == "application/json"
    assert request.json() == {"personUrl": "u", "retrieveExperience": True}


def test_non_ok_response_with_error_raises_linked_api_error(
    requests_mock: requests_mock.Mocker,
) -> None:
    requests_mock.get(
        "https://api.test/account",
        status_code=401,
        json={"error": {"type": "invalidLinkedApiToken", "message": "bad token"}},
    )
    client = LinkedApiHttpClient(
        LinkedApiConfig(
            linked_api_token="lat",
            identification_token="idt",
            base_url="https://api.test",
        )
    )

    with pytest.raises(LinkedApiError) as error:
        client.get("/account")

    assert error.value.type == "invalidLinkedApiToken"
    assert error.value.message == "bad token"


def test_network_error_raises_http_error(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get("https://api.test/account", exc=requests.exceptions.ConnectTimeout)
    client = LinkedApiHttpClient(
        LinkedApiConfig(
            linked_api_token="lat",
            identification_token="idt",
            base_url="https://api.test",
        )
    )

    with pytest.raises(LinkedApiError) as error:
        client.get("/account")

    assert error.value.type == "httpError"
