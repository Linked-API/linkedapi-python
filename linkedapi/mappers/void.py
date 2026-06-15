from __future__ import annotations

from typing import Generic, TypeVar

from linkedapi.mappers.base import (
    BaseMapper,
    MappedResponse,
    as_action_dict,
    collect_action_errors,
    parse_action_error,
)
from linkedapi.types import WorkflowCompletion, WorkflowDefinition, serialize_model

TParams = TypeVar("TParams")


class VoidWorkflowMapper(BaseMapper[TParams, None], Generic[TParams]):
    def __init__(self, action_type: str) -> None:
        self.action_type = action_type

    def map_request(self, params: TParams | None = None) -> WorkflowDefinition:
        return {"actionType": self.action_type, **serialize_model(params)}

    def map_response(self, completion: WorkflowCompletion) -> MappedResponse[None]:
        if isinstance(completion, list):
            errors = collect_action_errors(
                [as_action_dict(action).get("error") for action in completion]
            )
            return MappedResponse(data=None, errors=errors)

        action = as_action_dict(completion)
        error = parse_action_error(action.get("error"))
        return MappedResponse(data=None, errors=[] if error is None else [error])
