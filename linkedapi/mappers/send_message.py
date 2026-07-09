from __future__ import annotations

from typing import Any

from linkedapi.mappers.base import (
    BaseMapper,
    MappedResponse,
    as_action_dict,
    collect_action_errors,
)
from linkedapi.types import WorkflowCompletion, WorkflowDefinition, serialize_model
from linkedapi.types.message import SendMessageParams


class SendMessageMapper(BaseMapper[SendMessageParams, None]):
    def map_request(self, params: SendMessageParams | None = None) -> WorkflowDefinition:
        serialized = serialize_model(params)
        manage_conversation = serialized.pop("manageConversation", None)
        definition: dict[str, Any] = {"actionType": "st.sendMessage", **serialized}
        # The child st.manageConversation acts on the conversation this message was sent into, so it
        # carries only `operation` — no threadId. Core rejects a threadId on a child manageConversation.
        # Guard on `operation` so an empty passthrough (e.g. Make sending {"operation": ""}) is ignored.
        if manage_conversation and manage_conversation.get("operation"):
            definition["then"] = {
                "actionType": "st.manageConversation",
                "operation": manage_conversation["operation"],
            }
        return definition

    def map_response(self, completion: WorkflowCompletion) -> MappedResponse[None]:
        if isinstance(completion, list):
            errors = collect_action_errors(
                [as_action_dict(action).get("error") for action in completion]
            )
            return MappedResponse(data=None, errors=errors)

        action = as_action_dict(completion)
        raw_errors: list[Any] = [action.get("error")]

        single_data = action.get("data")
        if single_data is not None:
            then_actions = as_action_dict(single_data).get("then")
            if then_actions:
                child_actions = then_actions if isinstance(then_actions, list) else [then_actions]
                raw_errors.extend(as_action_dict(child).get("error") for child in child_actions)

        return MappedResponse(data=None, errors=collect_action_errors(raw_errors))
