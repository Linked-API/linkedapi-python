from __future__ import annotations

from typing import Any, Generic, TypeVar, cast

from pydantic import BaseModel

from linkedapi.mappers.base import (
    BaseMapper,
    MappedResponse,
    as_action_dict,
    collect_action_errors,
    parse_action_error,
    parse_result,
)
from linkedapi.types import WorkflowCompletion, WorkflowDefinition, serialize_model

TParams = TypeVar("TParams")
TResult = TypeVar("TResult")


class SimpleWorkflowMapper(BaseMapper[TParams, TResult], Generic[TParams, TResult]):
    def __init__(
        self,
        action_type: str,
        default_params: dict[str, Any] | None = None,
        result_model: type[BaseModel] | None = None,
    ) -> None:
        self.action_type = action_type
        self.default_params = default_params or {}
        self.result_model = result_model

    def map_request(self, params: TParams | None = None) -> WorkflowDefinition:
        return {"actionType": self.action_type, **self.default_params, **serialize_model(params)}

    def map_response(self, completion: WorkflowCompletion) -> MappedResponse[TResult]:
        if isinstance(completion, list):
            data = [
                as_action_dict(action).get("data")
                for action in completion
                if as_action_dict(action).get("data")
            ]
            errors = collect_action_errors(
                [as_action_dict(action).get("error") for action in completion]
            )
            return MappedResponse(
                data=cast(TResult, parse_result(data, self.result_model)), errors=errors
            )

        action = as_action_dict(completion)
        error = parse_action_error(action.get("error"))
        if error is not None:
            return MappedResponse(data=None, errors=[error])
        return MappedResponse(
            data=cast(TResult, parse_result(action.get("data"), self.result_model)),
            errors=[],
        )
