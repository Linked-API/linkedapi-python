from __future__ import annotations

import pytest
from conftest import FakeHttpClient

from linkedapi import (
    FetchPerson,
    LinkedApiError,
    LinkedApiWorkflowTimeoutError,
    MappedResponse,
    Operation,
    RetrieveSSI,
    VoidWorkflowMapper,
    WorkflowInProgressResponse,
    poll_workflow_result,
)


def test_operation_result_polls_until_completion(fake_http_client: FakeHttpClient) -> None:
    fake_http_client.queue_response(
        result={"workflowId": "wf1", "workflowStatus": "pending", "message": "queued"}
    )
    fake_http_client.queue_response(
        result={"workflowId": "wf1", "workflowStatus": "running", "message": "running"}
    )
    fake_http_client.queue_response(
        result={
            "workflowId": "wf1",
            "workflowStatus": "completed",
            "completion": {
                "actionType": "st.retrieveSSI",
                "success": True,
                "data": {"ssi": 77, "industryTop": 10, "networkTop": 20},
            },
        }
    )
    operation = RetrieveSSI(fake_http_client)

    result = operation.result("wf1", poll_interval=0.001, timeout=1.0)

    assert result.data is not None
    assert result.data.industry_top == 10
    assert [call[1] for call in fake_http_client.calls] == [
        "/workflows/wf1",
        "/workflows/wf1",
        "/workflows/wf1",
    ]


def test_operation_result_wraps_response_validation_error(
    fake_http_client: FakeHttpClient,
) -> None:
    fake_http_client.queue_response(
        result={
            "workflowId": "wf1",
            "workflowStatus": "completed",
            "completion": {
                "actionType": "st.openPersonPage",
                "success": True,
                "data": {"name": "Jane Doe", "experiences": [123]},
            },
        }
    )

    with pytest.raises(LinkedApiError) as error:
        FetchPerson(fake_http_client).result("wf1", poll_interval=0.001, timeout=1.0)

    assert error.value.type == "unknownError"
    assert error.value.message.startswith("Failed to parse API response:")
    assert isinstance(error.value.details, list)


def test_poll_workflow_result_timeout_is_plain_linked_api_error() -> None:
    def always_running() -> WorkflowInProgressResponse:
        return WorkflowInProgressResponse(workflow_id="wf1", workflow_status="running")

    with pytest.raises(LinkedApiError) as error:
        poll_workflow_result(always_running, poll_interval=0.001, timeout=0.003)

    assert error.value.type == "workflowTimeout"


class AlwaysRunningOperation(Operation[None, None]):
    operation_name = "sendMessage"
    mapper = VoidWorkflowMapper[None]("st.sendMessage")

    def status(self, workflow_id: str) -> WorkflowInProgressResponse | MappedResponse[None]:
        return WorkflowInProgressResponse(workflow_id=workflow_id, workflow_status="running")


def test_operation_result_wraps_timeout() -> None:
    operation = AlwaysRunningOperation(FakeHttpClient())

    with pytest.raises(LinkedApiWorkflowTimeoutError) as error:
        operation.result("wf1", poll_interval=0.001, timeout=0.003)

    assert error.value.workflow_id == "wf1"
    assert error.value.operation_name == "sendMessage"


def test_polling_rethrows_after_max_invalid_http_errors() -> None:
    calls = 0

    def always_http_error() -> MappedResponse[None]:
        nonlocal calls
        calls += 1
        raise LinkedApiError("httpError", "temporary")

    with pytest.raises(LinkedApiError) as error:
        poll_workflow_result(
            always_http_error,
            poll_interval=0.001,
            timeout=1.0,
            max_invalid_attempts=15,
        )

    assert error.value.type == "httpError"
    assert calls == 16
