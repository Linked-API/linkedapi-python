from __future__ import annotations

from abc import ABC
from typing import Any, Generic, TypeVar

from linkedapi.core.polling import poll_workflow_result
from linkedapi.errors import LinkedApiError, LinkedApiWorkflowTimeoutError
from linkedapi.http import HttpClient
from linkedapi.mappers import BaseMapper, MappedResponse
from linkedapi.types import (
    WorkflowCancelResponse,
    WorkflowCompletion,
    WorkflowInProgressResponse,
    WorkflowResponse,
    WorkflowStartedResponse,
)

TParams = TypeVar("TParams")
TResult = TypeVar("TResult")


class Operation(ABC, Generic[TParams, TResult]):
    operation_name: str
    mapper: BaseMapper[TParams, TResult]

    def __init__(self, http_client: HttpClient[Any]) -> None:
        self.http_client = http_client

    def execute(self, params: TParams | None = None) -> WorkflowStartedResponse:
        request = self.mapper.map_request(params)
        response = self.http_client.post("/workflows", request)
        if response.error:
            raise LinkedApiError(response.error.type, response.error.message)
        if response.result is None:
            raise LinkedApiError.unknown_error()
        return WorkflowStartedResponse.model_validate(response.result)

    def result(
        self,
        workflow_id: str,
        *,
        poll_interval: float | None = None,
        timeout: float | None = None,
    ) -> MappedResponse[TResult]:
        try:
            return poll_workflow_result(
                lambda: self.status(workflow_id),
                poll_interval=5.0 if poll_interval is None else poll_interval,
                timeout=86400.0 if timeout is None else timeout,
            )
        except LinkedApiError as error:
            if error.type == "workflowTimeout":
                raise LinkedApiWorkflowTimeoutError(workflow_id, self.operation_name) from error
            raise

    def status(self, workflow_id: str) -> WorkflowInProgressResponse | MappedResponse[TResult]:
        workflow_result = self._get_workflow_result(workflow_id)
        if workflow_result.workflow_status in {"running", "pending"}:
            return WorkflowInProgressResponse(
                workflow_id=workflow_id,
                workflow_status=workflow_result.workflow_status,
                message=workflow_result.message,
            )

        completion = self._get_completion(workflow_result)
        return self.mapper.map_response(completion)

    def cancel(self, workflow_id: str) -> bool:
        response = self.http_client.delete(f"/workflows/{workflow_id}")
        if response.error:
            raise LinkedApiError(response.error.type, response.error.message)
        if response.result is None:
            raise LinkedApiError.unknown_error()
        return WorkflowCancelResponse.model_validate(response.result).cancelled

    def _get_workflow_result(self, workflow_id: str) -> WorkflowResponse:
        response = self.http_client.get(f"/workflows/{workflow_id}")
        if response.error:
            raise LinkedApiError(response.error.type, response.error.message)
        if response.result is None:
            raise LinkedApiError.unknown_error()
        return WorkflowResponse.model_validate(response.result)

    def _get_completion(self, response: WorkflowResponse) -> WorkflowCompletion:
        if response.completion is None:
            if response.failure:
                raise LinkedApiError(response.failure.reason, response.failure.message)
            raise LinkedApiError.unknown_error()
        return response.completion
