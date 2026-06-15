from __future__ import annotations

from linkedapi import (
    FetchPersonParams,
    LimitParams,
    LimitSinceParams,
    NvSearchCompaniesParams,
    NvSearchPeopleParams,
    Person,
    SearchCompaniesParams,
    SearchPeopleParams,
)


def test_model_dump_uses_camel_case_aliases() -> None:
    params = FetchPersonParams(
        person_url="u",
        retrieve_experience=True,
        retrieve_posts=True,
        posts_retrieval_config={"limit": 10},
    )

    assert params.model_dump(by_alias=True, exclude_none=True) == {
        "personUrl": "u",
        "retrieveExperience": True,
        "retrievePosts": True,
        "postsRetrievalConfig": {"limit": 10},
    }
    assert isinstance(params.posts_retrieval_config, LimitParams)
    assert isinstance(params.posts_retrieval_config, LimitSinceParams)


def test_search_params_reuse_limit_params_and_dump_limit() -> None:
    for params in (
        SearchPeopleParams(limit=25, term="engineer"),
        NvSearchPeopleParams(limit=25, term="engineer"),
        SearchCompaniesParams(limit=25, term="api"),
        NvSearchCompaniesParams(limit=25, term="api"),
    ):
        assert isinstance(params, LimitParams)
        assert params.model_dump(by_alias=True, exclude_none=True)["limit"] == 25


def test_response_json_parses_to_snake_case_access() -> None:
    person = Person.model_validate(
        {
            "name": "Jane Doe",
            "publicUrl": "https://www.linkedin.com/in/jane-doe",
            "hashedUrl": "hash",
            "headline": "Founder",
            "location": "New York",
            "countryCode": "us",
            "position": "CEO",
            "companyName": "Acme",
            "companyHashedUrl": "company-hash",
            "followersCount": 42,
            "about": None,
        }
    )

    assert person.followers_count == 42
    assert person.company_hashed_url == "company-hash"
