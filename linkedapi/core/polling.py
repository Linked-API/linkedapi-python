from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar, cast

from linkedapi.errors import LinkedApiError
from linkedapi.types import WorkflowInProgressResponse

TResult = TypeVar("TResult")


def poll_workflow_result(
    workflow_result_fn: Callable[[], TResult | WorkflowInProgressResponse],
    *,
    poll_interval: float = 5.0,
    timeout: float = 86400.0,
    max_invalid_attempts: int = 15,
) -> TResult:
    start_time = time.monotonic()
    invalid_attempts = 0

    while time.monotonic() - start_time < timeout:
        try:
            result = workflow_result_fn()
            if not _is_workflow_in_progress(result):
                return cast(TResult, result)
            invalid_attempts = 0
        except LinkedApiError as error:
            if error.type == "httpError":
                invalid_attempts += 1
                if invalid_attempts > max_invalid_attempts:
                    raise
            else:
                raise

        remaining = timeout - (time.monotonic() - start_time)
        if remaining > 0:
            time.sleep(min(poll_interval, remaining))

    raise LinkedApiError("workflowTimeout", f"Workflow did not complete within {timeout}s")


def _is_workflow_in_progress(value: object) -> bool:
    status = getattr(value, "workflow_status", None)
    if isinstance(value, dict):
        status = value.get("workflowStatus") or value.get("workflow_status")
    return status in {"running", "pending"}
