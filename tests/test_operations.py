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
    SearchPostActor,
    SearchPostResult,
    SearchPostsCompanyFilter,
    SearchPostsFilter,
    SearchPostsParams,
    SearchPostsPersonFilter,
    SimpleWorkflowMapper,
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
        "search_posts",
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
        "react_to_comment",
        "reply_to_comment",
        "create_post",
        "create_repost",
        "retrieve_ssi",
        "retrieve_performance",
        "retrieve_profile_viewers",
    ]

    for name in operation_names:
        operation = getattr(linkedapi, name)
        assert hasattr(operation, "execute")
        assert hasattr(operation, "result")
        assert hasattr(operation, "cancel")
    assert len(linkedapi.operations) == 41


def test_operation_mappers_match_node_contract() -> None:
    linkedapi = LinkedApi(LinkedApiConfig(linked_api_token="x", identification_token="y"))

    assert linkedapi.fetch_person.mapper.base_action_type == "st.openPersonPage"
    assert linkedapi.fetch_person.mapper.default_params == {"basicInfo": True}
    assert isinstance(linkedapi.search_people.mapper, ArrayWorkflowMapper)
    assert linkedapi.search_people.mapper.base_action_type == "st.searchPeople"
    assert isinstance(linkedapi.search_jobs.mapper, ArrayWorkflowMapper)
    assert linkedapi.search_jobs.mapper.base_action_type == "st.searchJobs"
    assert isinstance(linkedapi.search_posts.mapper, ArrayWorkflowMapper)
    assert linkedapi.search_posts.mapper.base_action_type == "st.searchPosts"
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
    assert isinstance(linkedapi.react_to_comment.mapper, VoidWorkflowMapper)
    assert linkedapi.react_to_comment.mapper.action_type == "st.reactToComment"
    assert isinstance(linkedapi.comment_on_post.mapper, SimpleWorkflowMapper)
    assert linkedapi.comment_on_post.mapper.action_type == "st.commentOnPost"
    assert isinstance(linkedapi.reply_to_comment.mapper, SimpleWorkflowMapper)
    assert linkedapi.reply_to_comment.mapper.action_type == "st.replyToComment"


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


def test_search_posts_maps_filter_params_and_actors_without_urn() -> None:
    linkedapi = LinkedApi(LinkedApiConfig(linked_api_token="x", identification_token="y"))

    request = linkedapi.search_posts.mapper.map_request(
        SearchPostsParams(
            term="climate tech",
            limit=20,
            filter={
                "sort": "latest",
                "date_posted": "pastWeek",
                "content_type": "images",
                "posted_by": ["firstConnections", "peopleYouFollow"],
                "from_members": [{"name": "Bill Gates", "urn": "urn:li:member:251749025"}],
                "from_companies": ["Example Company"],
                "mentioning_members": [],
                "mentioning_companies": [],
                "author_companies": [
                    {"name": "Example Company", "urn": "urn:li:organization:1234567"}
                ],
                "author_industries": ["Software Development"],
            },
            custom_search_url=(
                "https://www.linkedin.com/search/results/content/?keywords=climate%20tech"
            ),
        )
    )

    assert request == {
        "actionType": "st.searchPosts",
        "term": "climate tech",
        "limit": 20,
        "filter": {
            "sort": "latest",
            "datePosted": "pastWeek",
            "contentType": "images",
            "postedBy": ["firstConnections", "peopleYouFollow"],
            "fromMembers": [{"name": "Bill Gates", "urn": "urn:li:member:251749025"}],
            "fromCompanies": ["Example Company"],
            "mentioningMembers": [],
            "mentioningCompanies": [],
            "authorCompanies": [{"name": "Example Company", "urn": "urn:li:organization:1234567"}],
            "authorIndustries": ["Software Development"],
        },
        "customSearchUrl": "https://www.linkedin.com/search/results/content/?keywords=climate%20tech",
    }

    response = linkedapi.search_posts.mapper.map_response(
        {
            "actionType": "st.searchPosts",
            "success": True,
            "data": [
                {
                    "url": "https://www.linkedin.com/feed/update/urn:li:activity:1",
                    "activityUrn": "urn:li:activity:1",
                    "time": "2023-01-01T09:15:00Z",
                    "type": "repost",
                    "author": {
                        "type": "company",
                        "name": "Example Company",
                        "companyUrl": "https://www.linkedin.com/company/example-company",
                    },
                    "reposter": {
                        "type": "person",
                        "name": "Example Reposter",
                        "profileUrl": "https://www.linkedin.com/in/example-reposter",
                        "headline": None,
                    },
                    "text": "Original post content about the webinar.",
                    "repostText": "A useful summary for anyone planning a launch.",
                    "hashtags": [],
                    "mentions": [],
                    "externalLinks": [],
                    "images": [],
                    "documentSlides": [],
                    "hasVideo": True,
                    "videoThumbnail": "https://media.licdn.com/dms/image/video-cover.jpg",
                    "hasPoll": False,
                    "reactionsCount": 6,
                    "commentsCount": 0,
                    "repostsCount": 1,
                }
            ],
        }
    )

    assert response.data is not None
    post = response.data[0]
    assert isinstance(post, SearchPostResult)
    assert post.activity_urn == "urn:li:activity:1"
    assert post.author is not None
    assert post.author.company_url == "https://www.linkedin.com/company/example-company"
    assert post.reposter is not None
    assert post.reposter.profile_url == "https://www.linkedin.com/in/example-reposter"
    assert post.video_thumbnail == "https://media.licdn.com/dms/image/video-cover.jpg"
    assert post.reposts_count == 1
    # A search result never resolves an actor urn, so the field must not exist on this surface.
    assert "urn" not in SearchPostActor.model_fields


def test_search_posts_actor_filters_accept_bare_strings_and_objects_mixed() -> None:
    params = SearchPostsParams(
        term="ai",
        filter=SearchPostsFilter(
            from_members=[
                "Bill Gates",
                SearchPostsPersonFilter(
                    name="Satya Nadella",
                    person_hashed_url="https://www.linkedin.com/in/ACoAAABC",
                ),
            ],
            from_companies=[
                "Acme",
                SearchPostsCompanyFilter(
                    name="Globex",
                    company_hashed_url="https://www.linkedin.com/company/1035",
                ),
            ],
        ),
    )

    assert params.model_dump(by_alias=True, exclude_none=True) == {
        "term": "ai",
        "filter": {
            "fromMembers": [
                "Bill Gates",
                {
                    "name": "Satya Nadella",
                    "personHashedUrl": "https://www.linkedin.com/in/ACoAAABC",
                },
            ],
            "fromCompanies": [
                "Acme",
                {
                    "name": "Globex",
                    "companyHashedUrl": "https://www.linkedin.com/company/1035",
                },
            ],
        },
    }

    with pytest.raises(ValidationError):
        SearchPostsFilter(sort="mostRecent")

    with pytest.raises(ValidationError):
        SearchPostsFilter(from_members=[{"urn": "urn:li:member:1"}])


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
