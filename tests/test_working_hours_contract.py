from __future__ import annotations

from typing import Any
from unittest.mock import Mock

import pytest

from linkedapi.core.operation import Operation
from linkedapi.errors import LINKED_API_ERROR_TYPES
from linkedapi.types import (
    WorkflowInProgressResponse,
    WorkflowResponse,
    WorkflowStartedResponse,
)


class _StubMapper:
    def map_request(self, params: Any) -> Any:
        return params

    def map_response(self, completion: Any) -> Any:
        return completion


class _StubOperation(Operation):  # type: ignore[type-arg]
    operation_name = "fetchPerson"

    def __init__(self, http_client: Any) -> None:
        super().__init__(http_client)
        self.mapper = _StubMapper()  # type: ignore[assignment]


def _operation(workflow_result: dict[str, Any]) -> _StubOperation:
    http_client = Mock()
    http_client.get.return_value = Mock(
        error=None,
        result=WorkflowResponse.model_validate(workflow_result),
    )
    return _StubOperation(http_client)


class TestPendingReasonModels:
    def test_in_progress_response_accepts_a_pending_reason(self) -> None:
        response = WorkflowInProgressResponse(
            workflowId="wf-1",
            workflowStatus="pending",
            pendingReason="outsideWorkingHours",
        )

        assert response.pending_reason == "outsideWorkingHours"

    def test_started_response_accepts_a_pending_reason(self) -> None:
        response = WorkflowStartedResponse(
            workflowId="wf-1",
            workflowStatus="pending",
            pendingReason="queued",
        )

        assert response.pending_reason == "queued"

    @pytest.mark.parametrize(
        "model",
        [WorkflowInProgressResponse, WorkflowStartedResponse, WorkflowResponse],
    )
    def test_field_is_optional_for_back_compat(self, model: Any) -> None:
        response = model(workflowId="wf-1", workflowStatus="running")

        assert response.pending_reason is None


class TestStatusCarriesPendingReason:
    def test_carries_the_outside_working_hours_reason(self) -> None:
        operation = _operation(
            {
                "workflowId": "wf-1",
                "workflowStatus": "pending",
                "pendingReason": "outsideWorkingHours",
            }
        )

        result = operation.status("wf-1")

        assert isinstance(result, WorkflowInProgressResponse)
        assert result.pending_reason == "outsideWorkingHours"

    def test_carries_the_queued_reason(self) -> None:
        operation = _operation(
            {"workflowId": "wf-1", "workflowStatus": "pending", "pendingReason": "queued"}
        )

        result = operation.status("wf-1")

        assert isinstance(result, WorkflowInProgressResponse)
        assert result.pending_reason == "queued"

    def test_keeps_none_when_the_api_sends_nothing(self) -> None:
        operation = _operation({"workflowId": "wf-1", "workflowStatus": "running"})

        result = operation.status("wf-1")

        assert isinstance(result, WorkflowInProgressResponse)
        assert result.pending_reason is None


class TestWorkingHoursErrorTypes:
    @pytest.mark.parametrize("error_type", ["outsideWorkingHours", "workingHoursWaitExpired"])
    def test_error_type_is_known(self, error_type: str) -> None:
        assert error_type in LINKED_API_ERROR_TYPES
