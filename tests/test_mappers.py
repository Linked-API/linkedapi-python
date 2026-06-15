from __future__ import annotations

import pytest

from linkedapi import (
    ArrayWorkflowMapper,
    FetchCompanyMapper,
    FetchPersonMapper,
    FetchPersonParams,
    LinkedApiActionError,
    LinkedApiError,
    SimpleWorkflowMapper,
    VoidWorkflowMapper,
)


def test_then_mapper_builds_then_actions_and_clears_root_params() -> None:
    request = FetchPersonMapper().map_request(
        FetchPersonParams(
            person_url="u",
            retrieve_experience=True,
            retrieve_posts=True,
            posts_retrieval_config={"limit": 5},
        )
    )

    assert request == {
        "actionType": "st.openPersonPage",
        "basicInfo": True,
        "personUrl": "u",
        "then": [
            {"actionType": "st.retrievePersonExperience"},
            {"actionType": "st.retrievePersonPosts", "limit": 5},
        ],
    }


def test_then_mapper_maps_child_data_and_errors(person_data: dict[str, object]) -> None:
    completion = {
        "actionType": "st.openPersonPage",
        "success": True,
        "data": {
            **person_data,
            "then": [
                {
                    "actionType": "st.retrievePersonExperience",
                    "success": True,
                    "data": [
                        {
                            "position": "CEO",
                            "companyName": "Acme",
                            "companyHashedUrl": "h",
                            "employmentType": "fullTime",
                            "locationType": "remote",
                            "description": "desc",
                            "duration": 12,
                            "startTime": "2020",
                            "endTime": None,
                            "location": "Remote",
                        }
                    ],
                },
                {
                    "actionType": "st.retrievePersonPosts",
                    "success": False,
                    "error": {"type": "retrievingNotAllowed", "message": "blocked"},
                },
            ],
        },
    }

    response = FetchPersonMapper().map_response(completion)

    assert response.data is not None
    assert response.data.experiences is not None
    assert response.data.experiences[0].company_name == "Acme"
    assert response.data.posts is None
    assert response.errors == [LinkedApiActionError(type="retrievingNotAllowed", message="blocked")]


def test_then_mapper_strips_empty_then_from_response(person_data: dict[str, object]) -> None:
    completion = {
        "actionType": "st.openPersonPage",
        "success": True,
        "data": {**person_data, "then": []},
    }

    response = FetchPersonMapper().map_response(completion)

    assert response.data is not None
    assert "then" not in response.data.model_dump(by_alias=True, exclude_none=True)


def test_completion_result_models_tolerate_missing_person_and_company_fields() -> None:
    person_response = FetchPersonMapper().map_response(
        {
            "actionType": "st.openPersonPage",
            "success": True,
            "data": {"name": "Jane Doe"},
        }
    )
    company_response = FetchCompanyMapper().map_response(
        {
            "actionType": "st.openCompanyPage",
            "success": True,
            "data": {"name": "Acme"},
        }
    )

    assert person_response.data is not None
    assert person_response.data.name == "Jane Doe"
    assert person_response.data.public_url is None
    assert person_response.data.company_hashed_url is None
    assert person_response.data.followers_count is None

    assert company_response.data is not None
    assert company_response.data.name == "Acme"
    assert company_response.data.public_url is None
    assert company_response.data.employees_count is None
    assert company_response.data.posts is None


def test_parse_result_wraps_invalid_nested_response_type() -> None:
    completion = {
        "actionType": "st.openPersonPage",
        "success": True,
        "data": {"name": "Jane Doe", "experiences": [123]},
    }

    with pytest.raises(LinkedApiError) as error:
        FetchPersonMapper().map_response(completion)

    assert error.value.type == "unknownError"
    assert error.value.message.startswith("Failed to parse API response:")
    assert isinstance(error.value.details, list)


def test_simple_array_and_void_mappers() -> None:
    simple = SimpleWorkflowMapper[dict[str, str], dict[str, str]]("x.action")
    assert simple.map_request({"foo": "bar"}) == {"actionType": "x.action", "foo": "bar"}
    assert simple.map_response(
        {"actionType": "x.action", "success": True, "data": {"ok": "yes"}}
    ).data == {"ok": "yes"}

    array = ArrayWorkflowMapper[dict[str, str], dict[str, str]]("x.array")
    assert array.map_response(
        {"actionType": "x.array", "success": True, "data": {"id": "1"}}
    ).data == [{"id": "1"}]

    void = VoidWorkflowMapper[dict[str, str]]("x.void")
    assert void.map_response({"actionType": "x.void", "success": True}).data is None
