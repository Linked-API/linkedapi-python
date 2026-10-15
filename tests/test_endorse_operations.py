from __future__ import annotations

from typing import Any

import pytest
import requests_mock

import linkedapi

PERSON_URL = "https://www.linkedin.com/in/example-person"
WORKFLOW_ID = "endorsement-workflow"
PATTERNS = [r"project\s*manage", "^scrum$", "business"]


@pytest.fixture
def client() -> linkedapi.LinkedApi:
    return linkedapi.LinkedApi(
        linkedapi.LinkedApiConfig(
            linked_api_token="test-linked-api-token",
            identification_token="test-identification-token",
            base_url="https://api.test",
        )
    )


def queue_workflow(mock: requests_mock.Mocker, completion: dict[str, Any]) -> None:
    mock.post(
        "https://api.test/workflows",
        json={
            "success": True,
            "result": {"workflowId": WORKFLOW_ID, "workflowStatus": "pending"},
        },
    )
    mock.get(
        f"https://api.test/workflows/{WORKFLOW_ID}",
        json={"success": True, "result": {"workflowStatus": "completed", "completion": completion}},
    )


def skills_completion(skills: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "actionType": "st.openPersonPage",
        "success": True,
        "data": {
            "then": {"actionType": "st.retrievePersonSkills", "success": True, "data": skills}
        },
    }


def test_endorse_person_skill_posts_one_root_action_and_maps_success(
    client: linkedapi.LinkedApi, requests_mock: requests_mock.Mocker
) -> None:
    queue_workflow(requests_mock, {"actionType": "st.endorsePersonSkill", "success": True})

    started = client.endorse_person_skill.execute(
        linkedapi.EndorsePersonSkillParams(person_url=PERSON_URL, skill_name="Project Management")
    )
    result = client.endorse_person_skill.result(started.workflow_id)

    request = requests_mock.request_history[0]
    assert request.method == "POST"
    assert request.url == "https://api.test/workflows"
    assert request.json() == {
        "actionType": "st.endorsePersonSkill",
        "personUrl": PERSON_URL,
        "skillName": "Project Management",
    }
    assert result.data is None
    assert result.errors == []
    assert requests_mock.request_history[1].url == f"https://api.test/workflows/{WORKFLOW_ID}"


@pytest.mark.parametrize(
    "error_type",
    [
        "personNotFound",
        "connectionNotFound",
        "skillNotFound",
        "endorsementUnavailable",
        "limitExceeded",
    ],
)
def test_endorse_person_skill_preserves_action_errors(
    client: linkedapi.LinkedApi, requests_mock: requests_mock.Mocker, error_type: str
) -> None:
    error = {"type": error_type, "message": f"Fixture {error_type}"}
    queue_workflow(
        requests_mock, {"actionType": "st.endorsePersonSkill", "success": False, "error": error}
    )

    started = client.endorse_person_skill.execute(
        linkedapi.EndorsePersonSkillParams(person_url=PERSON_URL, skill_name="Project Management")
    )
    result = client.endorse_person_skill.result(started.workflow_id)

    assert result.data is None
    assert [item.model_dump() for item in result.errors] == [error]


def test_endorse_person_skills_posts_patterns_and_maps_selection_in_profile_order(
    client: linkedapi.LinkedApi, requests_mock: requests_mock.Mocker
) -> None:
    unavailable = {"type": "endorsementUnavailable", "message": "Fixture unavailable"}
    disconnected = {"type": "connectionNotFound", "message": "Fixture disconnected"}
    queue_workflow(
        requests_mock,
        skills_completion(
            [
                {
                    "name": "Project Management",
                    "then": [{"actionType": "st.endorsePersonSkill", "success": True}],
                },
                {"name": "Python"},
                {
                    "name": "Business Strategy",
                    "then": [
                        {
                            "actionType": "st.endorsePersonSkill",
                            "success": False,
                            "error": unavailable,
                        }
                    ],
                },
                {
                    "name": "Scrum",
                    "then": [
                        {
                            "actionType": "st.endorsePersonSkill",
                            "success": False,
                            "error": disconnected,
                        }
                    ],
                },
            ]
        ),
    )

    started = client.endorse_person_skills.execute(
        linkedapi.EndorsePersonSkillsParams(person_url=PERSON_URL, skill_name_patterns=PATTERNS)
    )
    result = client.endorse_person_skills.result(started.workflow_id)

    assert requests_mock.request_history[0].json() == {
        "actionType": "st.openPersonPage",
        "personUrl": PERSON_URL,
        "basicInfo": False,
        "then": {
            "actionType": "st.retrievePersonSkills",
            "then": {
                "actionType": "st.doForSkills",
                "skillNamePatterns": PATTERNS,
                "then": {"actionType": "st.endorsePersonSkill"},
            },
        },
    }
    assert result.data is not None
    assert all(isinstance(item, linkedapi.PersonSkillEndorsement) for item in result.data)
    assert [item.model_dump(exclude_none=True) for item in result.data] == [
        {"skill_name": "Project Management", "success": True},
        {"skill_name": "Business Strategy", "success": False, "error": unavailable},
        {"skill_name": "Scrum", "success": False, "error": disconnected},
    ]
    assert result.errors == []


@pytest.mark.parametrize("options", [{}, {"skill_name_patterns": None}])
def test_endorse_person_skills_omits_absent_patterns_and_maps_every_skill(
    client: linkedapi.LinkedApi, requests_mock: requests_mock.Mocker, options: dict[str, Any]
) -> None:
    queue_workflow(
        requests_mock,
        skills_completion(
            [
                {
                    "name": "Business Strategy",
                    "then": [{"actionType": "st.endorsePersonSkill", "success": True}],
                },
                {
                    "name": "Python",
                    "then": [{"actionType": "st.endorsePersonSkill", "success": True}],
                },
            ]
        ),
    )

    started = client.endorse_person_skills.execute(
        linkedapi.EndorsePersonSkillsParams(person_url=PERSON_URL, **options)
    )
    result = client.endorse_person_skills.result(started.workflow_id)

    assert requests_mock.request_history[0].json() == {
        "actionType": "st.openPersonPage",
        "personUrl": PERSON_URL,
        "basicInfo": False,
        "then": {
            "actionType": "st.retrievePersonSkills",
            "then": {
                "actionType": "st.doForSkills",
                "then": {"actionType": "st.endorsePersonSkill"},
            },
        },
    }
    assert result.data is not None
    assert [item.model_dump(exclude_none=True) for item in result.data] == [
        {"skill_name": "Business Strategy", "success": True},
        {"skill_name": "Python", "success": True},
    ]
    assert result.errors == []


def test_endorse_person_skills_keeps_limit_errors_on_each_remaining_selected_skill(
    client: linkedapi.LinkedApi, requests_mock: requests_mock.Mocker
) -> None:
    error = {"type": "limitExceeded", "message": "Fixture endorsement cap"}
    queue_workflow(
        requests_mock,
        skills_completion(
            [
                {
                    "name": "Python",
                    "then": [{"actionType": "st.endorsePersonSkill", "success": True}],
                },
                {
                    "name": "Scrum",
                    "then": [
                        {"actionType": "st.endorsePersonSkill", "success": False, "error": error}
                    ],
                },
                {
                    "name": "Agile",
                    "then": [
                        {"actionType": "st.endorsePersonSkill", "success": False, "error": error}
                    ],
                },
            ]
        ),
    )

    started = client.endorse_person_skills.execute(
        linkedapi.EndorsePersonSkillsParams(person_url=PERSON_URL)
    )
    result = client.endorse_person_skills.result(started.workflow_id)

    assert result.data is not None
    assert [item.model_dump(exclude_none=True) for item in result.data] == [
        {"skill_name": "Python", "success": True},
        {"skill_name": "Scrum", "success": False, "error": error},
        {"skill_name": "Agile", "success": False, "error": error},
    ]
    assert result.errors == []


@pytest.mark.parametrize("stage", ["page", "skills"])
def test_endorse_person_skills_reports_parent_action_failure(
    client: linkedapi.LinkedApi, requests_mock: requests_mock.Mocker, stage: str
) -> None:
    error = {"type": "personNotFound", "message": "Fixture missing person"}
    failed = {
        "actionType": "st.openPersonPage" if stage == "page" else "st.retrievePersonSkills",
        "success": False,
        "error": error,
    }
    queue_workflow(
        requests_mock,
        failed
        if stage == "page"
        else {"actionType": "st.openPersonPage", "success": True, "data": {"then": failed}},
    )

    started = client.endorse_person_skills.execute(
        linkedapi.EndorsePersonSkillsParams(person_url=PERSON_URL)
    )
    result = client.endorse_person_skills.result(started.workflow_id)

    assert result.data is None
    assert [item.model_dump() for item in result.errors] == [error]


@pytest.mark.parametrize("skills", [[], [{"name": "Python"}]])
def test_endorse_person_skills_returns_empty_selection(
    client: linkedapi.LinkedApi, requests_mock: requests_mock.Mocker, skills: list[dict[str, Any]]
) -> None:
    queue_workflow(requests_mock, skills_completion(skills))

    started = client.endorse_person_skills.execute(
        linkedapi.EndorsePersonSkillsParams(person_url=PERSON_URL, skill_name_patterns=["^scrum$"])
    )
    result = client.endorse_person_skills.result(started.workflow_id)

    assert result.data == []
    assert result.errors == []
