from __future__ import annotations

from typing import Any, Literal

from linkedapi.errors import LinkedApiActionErrorType
from linkedapi.types.base import LinkedApiModel

WorkflowPendingStatus = Literal["pending"]
WorkflowRunningStatus = Literal["running"]
WorkflowInProgressStatus = Literal["pending", "running"]
WorkflowStatus = Literal["pending", "running", "completed", "failed"]
WorkflowDefinition = dict[str, Any] | list[dict[str, Any]]
WorkflowCompletion = dict[str, Any] | list[dict[str, Any]]


class LinkedApiActionError(LinkedApiModel):
    type: LinkedApiActionErrorType | str
    message: str


class WorkflowStartedResponse(LinkedApiModel):
    workflow_id: str
    workflow_status: WorkflowInProgressStatus
    message: str | None = None


class WorkflowInProgressResponse(LinkedApiModel):
    workflow_id: str
    workflow_status: WorkflowInProgressStatus
    message: str | None = None


class WorkflowFailure(LinkedApiModel):
    reason: str
    message: str


class WorkflowCancelResponse(LinkedApiModel):
    cancelled: bool


class WorkflowResponse(LinkedApiModel):
    workflow_id: str
    workflow_status: WorkflowStatus
    message: str | None = None
    completion: WorkflowCompletion | None = None
    failure: WorkflowFailure | None = None


class WorkflowCompletionSingleAction(LinkedApiModel):
    action_type: str
    success: bool
    data: Any | None = None
    error: LinkedApiActionError | None = None
    label: str | None = None
