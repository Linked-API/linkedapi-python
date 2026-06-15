from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast

from pydantic import BaseModel

from linkedapi.errors import LinkedApiError
from linkedapi.mappers.base import (
    BaseMapper,
    MappedResponse,
    as_action_dict,
    collect_action_errors,
    parse_action_error,
    parse_result,
)
from linkedapi.types import (
    WorkflowCompletion,
    WorkflowDefinition,
    dump_model_by_name,
    serialize_model,
)
from linkedapi.types.base import to_camel

TParams = TypeVar("TParams")
TResult = TypeVar("TResult")


@dataclass(frozen=True)
class ActionConfig:
    param_name: str
    action_type: str
    config_source: str | None = None


@dataclass(frozen=True)
class ResponseMapping:
    action_type: str
    target_property: str


class ThenWorkflowMapper(BaseMapper[TParams, TResult], Generic[TParams, TResult]):
    def __init__(
        self,
        action_configs: list[ActionConfig],
        response_mappings: list[ResponseMapping],
        base_action_type: str,
        default_params: dict[str, Any] | None = None,
        result_model: type[BaseModel] | None = None,
    ) -> None:
        self.action_configs = action_configs
        self.response_mappings = response_mappings
        self.base_action_type = base_action_type
        self.default_params = default_params or {}
        self.result_model = result_model

    def map_request(self, params: TParams | None = None) -> WorkflowDefinition:
        alias_params = serialize_model(params)
        name_params = dump_model_by_name(params)
        resolve_alias = _make_alias_resolver(params)
        then = self._build_then_for_request(alias_params, name_params, resolve_alias)
        clear_params = self._clear_params(alias_params, resolve_alias)
        return {
            "actionType": self.base_action_type,
            **self.default_params,
            **clear_params,
            "then": then,
        }

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
        single_data = action.get("data")
        if single_data is not None:
            return self._map_then_from_response(as_action_dict(single_data))
        raise LinkedApiError.unknown_error()

    def _map_then_from_response(self, data: dict[str, Any]) -> MappedResponse[TResult]:
        result = {**data}
        then_actions = data.get("then")
        errors: list[Any] = []

        if not then_actions:
            result.pop("then", None)
            return MappedResponse(
                data=cast(TResult, parse_result(result, self.result_model)),
                errors=[],
            )

        for mapping in self.response_mappings:
            if isinstance(then_actions, list) and then_actions:
                then_action = self._find_then_action(then_actions, mapping.action_type)
                if then_action is not None:
                    result[mapping.target_property] = then_action.get("data")
                    errors.append(then_action.get("error"))
                continue

            then_action = as_action_dict(then_actions)
            if then_action.get("actionType") == mapping.action_type:
                result[mapping.target_property] = then_action.get("data")
                errors.append(then_action.get("error"))

        result.pop("then", None)
        return MappedResponse(
            data=cast(TResult, parse_result(result, self.result_model)),
            errors=collect_action_errors(errors),
        )

    def _build_then_for_request(
        self,
        alias_params: dict[str, Any],
        name_params: dict[str, Any],
        resolve_alias: AliasResolver,
    ) -> list[dict[str, Any]]:
        actions: list[dict[str, Any]] = []
        for config in self.action_configs:
            if name_params.get(config.param_name) is True:
                action = {"actionType": config.action_type}
                if config.config_source:
                    action.update(alias_params.get(resolve_alias(config.config_source), {}))
                actions.append(action)
        return actions

    def _clear_params(
        self,
        params: dict[str, Any],
        resolve_alias: AliasResolver,
    ) -> dict[str, Any]:
        cleaned_params = {**params}
        for config in self.action_configs:
            cleaned_params.pop(resolve_alias(config.param_name), None)
            if config.config_source:
                cleaned_params.pop(resolve_alias(config.config_source), None)
        return cleaned_params

    def _find_then_action(self, actions: list[Any], action_type: str) -> dict[str, Any] | None:
        for action in actions:
            action_dict = as_action_dict(action)
            if action_dict.get("actionType") == action_type:
                return action_dict
        return None


AliasResolver = Callable[[str], str]


def _make_alias_resolver(params: Any) -> AliasResolver:
    """Resolve a field's serialized key from the params model, mirroring its
    explicit pydantic alias (e.g. ``retrieve_dms`` -> ``retrieveDMs``) and
    falling back to ``to_camel`` for fields without one."""
    fields = type(params).model_fields if isinstance(params, BaseModel) else {}

    def resolve(name: str) -> str:
        field = fields.get(name)
        if field is not None and field.alias:
            return field.alias
        return to_camel(name)

    return resolve
