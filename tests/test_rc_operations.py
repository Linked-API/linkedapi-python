from __future__ import annotations

from typing import Any

import pytest
from conftest import FakeHttpClient

from linkedapi import (
    LinkedApi,
    RcArchiveProjectParams,
    RcCreateProjectParams,
    RcOpenPersonPageParams,
    RcRenameProjectParams,
    RcRetrieveProjectCandidatesParams,
    RcRetrieveProjectsParams,
    RcSaveToProjectParams,
    RcSearchPeopleParams,
    RcSendMessageParams,
    RcSyncInboxParams,
)

PERSON_URL = "https://www.linkedin.com/talent/profile/AEMAAB0xExampleProfileId1"
PROJECT_ID = "1700000003"
PERSON = {
    "name": "Jane Example",
    "recruiterProfileUrl": PERSON_URL,
    "headline": "Engineer",
    "location": "Berlin, Germany",
    "avatarUrl": None,
    "viewerState": {"connectionDegree": "3rd+"},
}
PROJECT = {
    "projectId": PROJECT_ID,
    "name": "Engineers",
    "createdAt": "2026-11-13T00:00:00.000Z",
    "candidateCount": 2,
    "projectUrl": f"https://www.linkedin.com/talent/hire/{PROJECT_ID}/overview",
}


@pytest.mark.parametrize(
    "method,action,params,request_data,result_data",
    [
        (
            "rc_search_people",
            "rc.searchPeople",
            RcSearchPeopleParams(term="engineer", limit=1),
            {"term": "engineer", "limit": 1},
            [PERSON],
        ),
        (
            "rc_fetch_person",
            "rc.openPersonPage",
            RcOpenPersonPageParams(person_url=PERSON_URL, recruiting_activity=True),
            {"personUrl": PERSON_URL, "basicInfo": True, "recruitingActivity": True, "then": []},
            {
                **PERSON,
                "publicUrl": "https://www.linkedin.com/in/jane-example",
                "industry": None,
                "recruitingActivity": {
                    "projects": 2,
                    "messages": 1,
                    "feedback": 0,
                    "attachments": 1,
                },
            },
        ),
        (
            "rc_retrieve_projects",
            "rc.retrieveProjects",
            RcRetrieveProjectsParams(limit=5),
            {"limit": 5},
            [PROJECT],
        ),
        (
            "rc_retrieve_project_candidates",
            "rc.retrieveProjectCandidates",
            RcRetrieveProjectCandidatesParams(project_id=PROJECT_ID, stage="contacted", limit=2),
            {"projectId": PROJECT_ID, "stage": "contacted", "limit": 2},
            [{**PERSON, "stage": "contacted"}],
        ),
        (
            "rc_save_to_project",
            "rc.saveToProject",
            RcSaveToProjectParams(project_id=PROJECT_ID, person_url=PERSON_URL),
            {"projectId": PROJECT_ID, "personUrl": PERSON_URL},
            {"alreadyInProject": True},
        ),
        (
            "rc_create_project",
            "rc.createProject",
            RcCreateProjectParams(name="  Engineers  "),
            {"name": "Engineers"},
            {"projectId": PROJECT_ID, "projectUrl": PROJECT["projectUrl"], "name": None},
        ),
        (
            "rc_rename_project",
            "rc.renameProject",
            RcRenameProjectParams(project_id=PROJECT_ID, name="Engineers", description="A\r\nB"),
            {"projectId": PROJECT_ID, "name": "Engineers", "description": "A\nB"},
            None,
        ),
        (
            "rc_archive_project",
            "rc.archiveProject",
            RcArchiveProjectParams(project_id=PROJECT_ID),
            {"projectId": PROJECT_ID},
            {"alreadyArchived": True},
        ),
        (
            "rc_send_message",
            "rc.sendMessage",
            RcSendMessageParams(person_url=PERSON_URL, subject="Role", text="Hello"),
            {"personUrl": PERSON_URL, "subject": "Role", "text": "Hello"},
            {"creditUsed": False},
        ),
        ("rc_sync_inbox", "rc.syncInbox", RcSyncInboxParams(), {}, None),
    ],
)
def test_recruiter_operation_request_and_result_contracts(
    fake_http_client: FakeHttpClient,
    method: str,
    action: str,
    params: Any,
    request_data: dict[str, Any],
    result_data: Any,
) -> None:
    sdk = LinkedApi(fake_http_client)
    op = getattr(sdk, method)
    assert op in sdk.operations
    assert op.operation_name == "rc" + "".join(part.title() for part in method.split("_")[1:])
    fake_http_client.queue_response(result={"workflowId": "rc1", "workflowStatus": "pending"})
    completion = {"actionType": action, "success": True}
    if result_data is not None:
        completion["data"] = result_data
    fake_http_client.queue_response(
        result={"workflowStatus": "completed", "completion": completion}
    )

    started = op.execute(params)
    result = op.result(started.workflow_id)

    assert fake_http_client.calls[0] == (
        "POST",
        "/workflows",
        {"actionType": action, **request_data},
    )
    assert result.errors == []
    if isinstance(result.data, list):
        assert [row.model_dump(by_alias=True) for row in result.data] == result_data
    elif result.data is not None:
        assert result.data.model_dump(by_alias=True) == result_data
    else:
        assert result_data is None


def test_search_keeps_every_filter_field_and_linkedin_language_codes(
    fake_http_client: FakeHttpClient,
) -> None:
    filters = {
        "jobTitles": ["Engineer"],
        "locations": ["Berlin"],
        "skills": ["Python"],
        "companies": ["Acme"],
        "currentCompanies": ["Current"],
        "pastCompanies": ["Past"],
        "schools": ["University"],
        "industries": ["Software"],
        "firstNames": ["Jane"],
        "lastNames": ["Example"],
        "groups": ["Developers"],
        "projects": ["Engineers"],
        "notes": ["Follow up"],
        "jobTitlesScope": "current",
        "companiesScope": "pastNotCurrent",
        "locationsScope": "currentOrOpenToRelocate",
        "companySizes": ["selfEmployed", "10001+"],
        "jobFunctions": ["Engineering"],
        "seniority": ["senior"],
        "yearsOfExperience": {"from": 1, "to": 5},
        "profileLanguages": ["en", "es", "in", "_o"],
        "networkRelationships": ["1st", "groupMembers", "3rd+"],
        "recentlyJoined": ["1day"],
        "hasPassedSkillAssessment": False,
        "isMilitaryVeteran": False,
        "hidePreviouslyViewed": True,
        "postalCode": {"code": "10115", "radiusMiles": 25},
        "graduationYears": {"from": 2000, "to": 2010},
        "recruitingActivity": {"type": "notes", "period": "pastYear"},
    }
    sdk = LinkedApi(fake_http_client)
    params = RcSearchPeopleParams.model_validate({"filter": filters, "limit": 25})
    assert sdk.rc_search_people.mapper.map_request(params) == {
        "actionType": "rc.searchPeople",
        "filter": filters,
        "limit": 25,
    }
    url = "https://www.linkedin.com/talent/search?keywords=engineer"
    assert sdk.rc_search_people.mapper.map_request(RcSearchPeopleParams(custom_search_url=url)) == {
        "actionType": "rc.searchPeople",
        "customSearchUrl": url,
    }


def test_fetch_person_can_request_activity_without_basic_info(
    fake_http_client: FakeHttpClient,
) -> None:
    op = LinkedApi(fake_http_client).rc_fetch_person
    assert op.mapper.map_request(
        RcOpenPersonPageParams(person_url=PERSON_URL, basic_info=False, recruiting_activity=True)
    ) == {
        "actionType": "rc.openPersonPage",
        "personUrl": PERSON_URL,
        "basicInfo": False,
        "recruitingActivity": True,
        "then": [],
    }
    data = {"recruitingActivity": {"projects": 0, "messages": 1, "feedback": 0, "attachments": 0}}
    result = op.mapper.map_response(
        {"actionType": "rc.openPersonPage", "success": True, "data": data}
    )
    assert result.data is not None
    assert result.data.recruiting_activity is not None
    assert result.data.recruiting_activity.messages == 1
    empty = op.mapper.map_response({"actionType": "rc.openPersonPage", "success": True, "data": {}})
    assert empty.data is not None
    assert empty.data.name is None


@pytest.mark.parametrize("paid", [True, False])
def test_send_keeps_explicit_credit_permission_and_reply_target(
    fake_http_client: FakeHttpClient,
    paid: bool,
) -> None:
    op = LinkedApi(fake_http_client).rc_send_message
    assert op.mapper.map_request(
        RcSendMessageParams(
            person_url=PERSON_URL, subject="Role", text="Hello", allow_paid_credit=paid
        )
    ) == {
        "actionType": "rc.sendMessage",
        "personUrl": PERSON_URL,
        "subject": "Role",
        "text": "Hello",
        "allowPaidCredit": paid,
    }
    assert op.mapper.map_request(RcSendMessageParams(thread_id="thread1", text="Reply")) == {
        "actionType": "rc.sendMessage",
        "threadId": "thread1",
        "text": "Reply",
    }


def test_sync_inbox_accepts_no_params(fake_http_client: FakeHttpClient) -> None:
    sdk = LinkedApi(fake_http_client)
    fake_http_client.queue_response(result={"workflowId": "sync", "workflowStatus": "pending"})
    sdk.rc_sync_inbox.execute()
    assert fake_http_client.calls == [("POST", "/workflows", {"actionType": "rc.syncInbox"})]
    assert not hasattr(sdk, "rc_do_for_people")
