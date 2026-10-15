from __future__ import annotations

from typing import Any, cast

from linkedapi.errors import LinkedApiError
from linkedapi.mappers.base import (
    BaseMapper,
    MappedResponse,
    as_action_dict,
    parse_action_error,
    parse_result,
)
from linkedapi.types import (
    EndorsePersonSkillsParams,
    PersonSkillEndorsement,
    WorkflowCompletion,
    WorkflowDefinition,
    serialize_model,
)


class EndorsePersonSkillsMapper(
    BaseMapper[EndorsePersonSkillsParams, list[PersonSkillEndorsement]]
):
    def map_request(self, params: EndorsePersonSkillsParams | None = None) -> WorkflowDefinition:
        serialized = serialize_model(params)
        skill_name_patterns = serialized.pop("skillNamePatterns", None)
        do_for_skills: dict[str, Any] = {
            "actionType": "st.doForSkills",
            "then": {"actionType": "st.endorsePersonSkill"},
        }
        if skill_name_patterns is not None:
            do_for_skills["skillNamePatterns"] = skill_name_patterns

        return {
            "actionType": "st.openPersonPage",
            "basicInfo": False,
            **serialized,
            "then": {"actionType": "st.retrievePersonSkills", "then": do_for_skills},
        }

    def map_response(
        self, completion: WorkflowCompletion
    ) -> MappedResponse[list[PersonSkillEndorsement]]:
        action = as_action_dict(completion)
        error = parse_action_error(action.get("error"))
        if error is not None:
            return MappedResponse(data=None, errors=[error])

        data = action.get("data")
        if data is None:
            raise LinkedApiError.unknown_error()
        then_actions = as_action_dict(data).get("then")
        child_actions = then_actions if isinstance(then_actions, list) else [then_actions]
        for child in child_actions:
            skills_action = as_action_dict(child)
            if skills_action.get("actionType") == "st.retrievePersonSkills":
                return self._map_skills(skills_action)
        raise LinkedApiError.unknown_error()

    def _map_skills(self, action: dict[str, Any]) -> MappedResponse[list[PersonSkillEndorsement]]:
        error = parse_action_error(action.get("error"))
        if error is not None:
            return MappedResponse(data=None, errors=[error])

        selected_skills: list[dict[str, Any]] = []
        for skill in action["data"]:
            for child in skill.get("then", []):
                endorsement = as_action_dict(child)
                if endorsement.get("actionType") == "st.endorsePersonSkill":
                    selected_skills.append(
                        {
                            "skillName": skill["name"],
                            "success": endorsement["success"],
                            "error": endorsement.get("error"),
                        }
                    )
                    break
        return MappedResponse(
            data=cast(
                list[PersonSkillEndorsement], parse_result(selected_skills, PersonSkillEndorsement)
            ),
            errors=[],
        )
