from __future__ import annotations

from typing import Generic, TypeVar, cast

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
TItem = TypeVar("TItem")


class ArrayWorkflowMapper(BaseMapper[TParams, list[TItem]], Generic[TParams, TItem]):
    def __init__(self, base_action_type: str, item_model: type[BaseModel] | None = None) -> None:
        self.base_action_type = base_action_type
        self.item_model = item_model

    def map_request(self, params: TParams | None = None) -> WorkflowDefinition:
        return {"actionType": self.base_action_type, **serialize_model(params)}

    def map_response(self, completion: WorkflowCompletion) -> MappedResponse[list[TItem]]:
        if isinstance(completion, list):
            data = [as_action_dict(action).get("data") for action in completion]
            errors = collect_action_errors(
                [as_action_dict(action).get("error") for action in completion]
            )
            return MappedResponse(
                data=cast(list[TItem], parse_result(data, self.item_model)), errors=errors
            )

        action = as_action_dict(completion)
        error = parse_action_error(action.get("error"))
        if error is not None:
            return MappedResponse(data=None, errors=[error])

        single_data = action.get("data")
        data_list = single_data if isinstance(single_data, list) else [single_data]
        return MappedResponse(
            data=cast(list[TItem], parse_result(data_list, self.item_model)),
            errors=[],
        )
