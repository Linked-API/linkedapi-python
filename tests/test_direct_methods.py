from __future__ import annotations

import pytest
from conftest import FakeHttpClient

from linkedapi import (
    ApiUsageParams,
    ConversationPollRequest,
    InboxPollRequest,
    LinkedApi,
    LinkedApiActionError,
    LinkedApiError,
    LinkedApiRequestError,
)


def test_poll_conversations_success(fake_http_client: FakeHttpClient) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_response(
        result=[
            {
                "personUrl": "u",
                "type": "st",
                "messages": [{"id": "m1", "sender": "them", "text": "hi", "time": "now"}],
            }
        ]
    )

    result = linkedapi.poll_conversations([ConversationPollRequest(person_url="u", type="st")])

    assert fake_http_client.calls[0] == (
        "POST",
        "/conversations/poll",
        [{"personUrl": "u", "type": "st"}],
    )
    assert result.data is not None
    assert result.data[0].messages[0].sender == "them"
    assert result.errors == []


def test_poll_conversations_response_error_maps_to_action_errors(
    fake_http_client: FakeHttpClient,
) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_response(
        success=False,
        error=LinkedApiRequestError(type="invalidRequestPayload", message="bad"),
    )

    result = linkedapi.poll_conversations([ConversationPollRequest(person_url="u", type="st")])

    assert result.data is None
    assert result.errors == [LinkedApiActionError(type="invalidRequestPayload", message="bad")]


def test_poll_conversations_thrown_conversations_not_synced_is_returned(
    fake_http_client: FakeHttpClient,
) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_error(LinkedApiError("conversationsNotSynced", "sync first"))

    result = linkedapi.poll_conversations([ConversationPollRequest(person_url="u", type="st")])

    assert result.data is None
    assert result.errors == [
        LinkedApiActionError(type="conversationsNotSynced", message="sync first")
    ]


def test_poll_conversations_other_thrown_error_is_raised(fake_http_client: FakeHttpClient) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_error(LinkedApiError("httpError", "broken"))

    with pytest.raises(LinkedApiError) as error:
        linkedapi.poll_conversations([ConversationPollRequest(person_url="u", type="st")])

    assert error.value.type == "httpError"


def test_poll_inbox_success(fake_http_client: FakeHttpClient) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_response(
        result={
            "messages": [
                {
                    "id": "m1",
                    "type": "st",
                    "threadId": "t1",
                    "personUrl": "u",
                    "sender": "them",
                    "text": "hi",
                    "time": "now",
                }
            ]
        }
    )

    result = linkedapi.poll_inbox(InboxPollRequest(type="st", thread_id="t1"))

    assert fake_http_client.calls[0] == (
        "POST",
        "/inbox/poll",
        {"type": "st", "threadId": "t1"},
    )
    assert result.data is not None
    assert result.data[0].thread_id == "t1"
    assert result.data[0].sender == "them"
    assert result.errors == []


def test_poll_inbox_without_request_sends_empty_body(fake_http_client: FakeHttpClient) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_response(result={"messages": []})

    result = linkedapi.poll_inbox()

    assert fake_http_client.calls[0] == ("POST", "/inbox/poll", {})
    assert result.data == []
    assert result.errors == []


def test_poll_inbox_response_error_maps_to_action_errors(
    fake_http_client: FakeHttpClient,
) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_response(
        success=False,
        error=LinkedApiRequestError(type="invalidRequestPayload", message="bad"),
    )

    result = linkedapi.poll_inbox(InboxPollRequest(type="st"))

    assert result.data is None
    assert result.errors == [LinkedApiActionError(type="invalidRequestPayload", message="bad")]


def test_get_account_info_and_api_usage_paths(fake_http_client: FakeHttpClient) -> None:
    linkedapi = LinkedApi(fake_http_client)
    fake_http_client.queue_response(result={"name": "Jane", "url": "https://linkedin.com/in/jane"})
    fake_http_client.queue_response(
        result=[{"actionType": "st.openPersonPage", "success": True, "time": "2026-01-01"}]
    )

    account = linkedapi.get_account_info()
    usage = linkedapi.get_api_usage(ApiUsageParams(start="2026-01-01", end="2026-01-02"))

    assert fake_http_client.calls == [
        ("GET", "/account", None),
        ("GET", "/stats/actions?start=2026-01-01&end=2026-01-02", None),
    ]
    assert account.data is not None
    assert account.data.name == "Jane"
    assert usage.data is not None
    assert usage.data[0].action_type == "st.openPersonPage"
