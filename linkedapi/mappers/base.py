from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ValidationError

from linkedapi.errors import LinkedApiError
from linkedapi.types import LinkedApiActionError, WorkflowCompletion, WorkflowDefinition

TParams = TypeVar("TParams")
TResult = TypeVar("TResult")


@dataclass
class MappedResponse(Generic[TResult]):
    data: TResult | None = None
    errors: list[LinkedApiActionError] = field(default_factory=list)


class BaseMapper(ABC, Generic[TParams, TResult]):
    @abstractmethod
    def map_request(self, params: TParams | None = None) -> WorkflowDefinition:
        raise NotImplementedError

    @abstractmethod
    def map_response(self, completion: WorkflowCompletion) -> MappedResponse[TResult]:
        raise NotImplementedError


def parse_action_error(value: Any) -> LinkedApiActionError | None:
    if value is None:
        return None
    if isinstance(value, LinkedApiActionError):
        return value
    return LinkedApiActionError.model_validate(value)


def collect_action_errors(values: list[Any]) -> list[LinkedApiActionError]:
    errors: list[LinkedApiActionError] = []
    for value in values:
        parsed = parse_action_error(value)
        if parsed is not None:
            errors.append(parsed)
    return errors


def parse_result(data: Any, model: type[BaseModel] | None) -> Any:
    if data is None or model is None:
        return data
    try:
        if isinstance(data, list):
            return [model.model_validate(item) for item in data]
        return model.model_validate(data)
    except ValidationError as error:
        raise LinkedApiError(
            "unknownError",
            f"Failed to parse API response: {error}",
            details=error.errors(),
        ) from error


def as_action_dict(action: Any) -> dict[str, Any]:
    if isinstance(action, BaseModel):
        return action.model_dump(by_alias=True, exclude_none=True)
    if isinstance(action, dict):
        return action
    msg = "Expected action object"
    raise TypeError(msg)
