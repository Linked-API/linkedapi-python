from __future__ import annotations

import pytest
from conftest import FakeHttpClient
from pydantic import ValidationError

from linkedapi import (
    AcceptInvitationParams,
    ArrayWorkflowMapper,
    FeedPost,
    FetchPersonParams,
    Invitation,
    LinkedApi,
    LinkedApiConfig,
    RetrieveFeedParams,
    VoidWorkflowMapper,
)


def test_linked_api_exposes_all_predefined_operations() -> None:
    linkedapi = LinkedApi(LinkedApiConfig(linked_api_token="x", identification_token="y"))
    operation_names = [
        "custom_workflow",
        "fetch_person",
        "nv_fetch_person",
        "fetch_company",
        "nv_fetch_company",
        "fetch_post",
        "fetch_job",
        "search_people",
        "nv_search_people",
        "search_companies",
        "nv_search_companies",
        "search_jobs",
        "send_connection_request",
        "check_connection_status",
        "withdraw_connection_request",
        "accept_invitation",
        "ignore_invitation",
        "retrieve_pending_requests",
        "retrieve_invitations",
        "retrieve_connections",
        "retrieve_feed",
        "remove_connection",
        "send_message",
        "sync_conversation",
        "sync_inbox",
        "sync_network",
        "manage_conversation",
        "nv_send_message",
        "nv_sync_conversation",
        "nv_sync_inbox",
        "nv_manage_conversation",
        "react_to_post",
        "comment_on_post",
        "create_post",
        "retrieve_ssi",
        "retrieve_performance",
    ]

    for name in operation_names:
        operation = getattr(linkedapi, name)
        assert hasattr(operation, "execute")
        assert hasattr(operation, "result")
        assert hasattr(operation, "cancel")
    assert len(linkedapi.operations) == 36


def test_operation_mappers_match_node_contract() -> None:
    linkedapi = LinkedApi(LinkedApiConfig(linked_api_token="x", identification_token="y"))

    assert linkedapi.fetch_person.mapper.base_action_type == "st.openPersonPage"
    assert linkedapi.fetch_person.mapper.default_params == {"basicInfo": True}
    assert isinstance(linkedapi.search_people.mapper, ArrayWorkflowMapper)
    assert linkedapi.search_people.mapper.base_action_type == "st.searchPeople"
    assert isinstance(linkedapi.search_jobs.mapper, ArrayWorkflowMapper)
    assert linkedapi.search_jobs.mapper.base_action_type == "st.searchJobs"
    assert linkedapi.fetch_job.mapper.base_action_type == "st.openJob"
    assert linkedapi.fetch_job.mapper.default_params == {"basicInfo": True}
    assert isinstance(linkedapi.send_connection_request.mapper, VoidWorkflowMapper)
    assert linkedapi.send_connection_request.mapper.action_type == "st.sendConnectionRequest"
    assert isinstance(linkedapi.accept_invitation.mapper, VoidWorkflowMapper)
    assert linkedapi.accept_invitation.mapper.action_type == "st.acceptInvitation"
    assert isinstance(linkedapi.ignore_invitation.mapper, VoidWorkflowMapper)
    assert linkedapi.ignore_invitation.mapper.action_type == "st.ignoreInvitation"
    assert isinstance(linkedapi.retrieve_invitations.mapper, ArrayWorkflowMapper)
    assert linkedapi.retrieve_invitations.mapper.base_action_type == "st.retrieveInvitations"
    assert isinstance(linkedapi.retrieve_feed.mapper, ArrayWorkflowMapper)
    assert linkedapi.retrieve_feed.mapper.base_action_type == "st.retrieveFeed"
    assert isinstance(linkedapi.sync_inbox.mapper, VoidWorkflowMapper)
    assert linkedapi.sync_inbox.mapper.action_type == "st.syncInbox"
    assert isinstance(linkedapi.nv_sync_inbox.mapper, VoidWorkflowMapper)
    assert linkedapi.nv_sync_inbox.mapper.action_type == "nv.syncInbox"
    assert isinstance(linkedapi.manage_conversation.mapper, VoidWorkflowMapper)
    assert linkedapi.manage_conversation.mapper.action_type == "st.manageConversation"
    assert isinstance(linkedapi.nv_manage_conversation.mapper, VoidWorkflowMapper)
    assert linkedapi.nv_manage_conversation.mapper.action_type == "nv.manageConversation"


def test_retrieve_feed_maps_params_and_feed_context() -> None:
    linkedapi = LinkedApi(LinkedApiConfig(linked_api_token="x", identification_token="y"))

    request = linkedapi.retrieve_feed.mapper.map_request(RetrieveFeedParams(limit=25))
    response = linkedapi.retrieve_feed.mapper.map_response(
        {
            "actionType": "st.retrieveFeed",
            "success": True,
            "data": [
                {
                    "url": "https://www.linkedin.com/feed/update/urn:li:activity:1",
                    "feedContext": "Example Person reacted to this",
                }
            ],
        }
    )

    assert request == {"actionType": "st.retrieveFeed", "limit": 25}
    assert response.data is not None
    assert isinstance(response.data[0], FeedPost)
    assert response.data[0].feed_context == "Example Person reacted to this"

    for invalid_limit in (0, 101):
        with pytest.raises(ValidationError):
            RetrieveFeedParams(limit=invalid_limit)


def test_invitation_params_require_the_matching_target_url() -> None:
    params = AcceptInvitationParams(
        invitation_type="companyFollow",
        company_url="https://www.linkedin.com/company/example/",
    )

    assert params.model_dump(by_alias=True, exclude_none=True) == {
        "invitationType": "companyFollow",
        "companyUrl": "https://www.linkedin.com/company/example/",
    }

    with pytest.raises(ValidationError):
        AcceptInvitationParams(
            invitation_type="newsletterSubscribe",
            person_url="https://www.linkedin.com/in/example/",
        )

    with pytest.raises(ValidationError):
        AcceptInvitationParams(
            invitation_type="connect",
            person_url="https://www.linkedin.com/in/example/",
            company_url="https://www.linkedin.com/company/example/",
        )


def test_invitation_result_fields_depend_on_type() -> None:
    connect = Invitation.model_validate(
        {
            "invitationType": "connect",
            "name": "Example Person",
            "publicUrl": "https://www.linkedin.com/in/example/",
            "headline": None,
            "note": None,
        }
    )
    assert connect.invitation_type == "connect"

    company_follow = Invitation.model_validate(
        {
            "invitationType": "companyFollow",
            "name": "Example Person",
            "publicUrl": "https://www.linkedin.com/in/example/",
            "companyUrl": "https://www.linkedin.com/company/example/",
            "companyName": None,
        }
    )
    assert company_follow.company_url == "https://www.linkedin.com/company/example/"

    with pytest.raises(ValidationError):
        Invitation.model_validate(
            {
                "invitationType": "connect",
                "name": "Example Person",
                "publicUrl": "https://www.linkedin.com/in/example/",
                "headline": None,
            }
        )

    with pytest.raises(ValidationError):
        Invitation.model_validate(
            {
                "invitationType": "companyFollow",
                "name": "Example Person",
                "publicUrl": "https://www.linkedin.com/in/example/",
                "companyUrl": "https://www.linkedin.com/company/example/",
                "companyName": None,
                "note": None,
            }
        )


def test_execute_and_result_flow_returns_pydantic_data(
    fake_http_client: FakeHttpClient,
    person_data: dict[str, object],
) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_response(result={"workflowId": "wf1", "workflowStatus": "pending"})
    fake_http_client.queue_response(
        result={
            "workflowId": "wf1",
            "workflowStatus": "completed",
            "completion": {
                "actionType": "st.openPersonPage",
                "success": True,
                "data": person_data,
            },
        }
    )

    workflow = linkedapi.fetch_person.execute(FetchPersonParams(person_url="u"))
    result = linkedapi.fetch_person.result(workflow.workflow_id, poll_interval=0.001, timeout=1.0)

    assert fake_http_client.calls[0] == (
        "POST",
        "/workflows",
        {
            "actionType": "st.openPersonPage",
            "basicInfo": True,
            "personUrl": "u",
            "then": [],
        },
    )
    assert result.data is not None
    assert result.data.public_url == "https://www.linkedin.com/in/jane-doe"
