from __future__ import annotations

import json
from typing import Any

import pytest
from conftest import FakeHttpClient

from linkedapi import (
    CreateSignalParams,
    GetSignalsParams,
    LinkedApi,
    LinkedApiError,
    LinkedApiRequestError,
    SetWebhookParams,
    SignalIdParams,
    SignalPollRequest,
    SignalPostSearchFilter,
    SignalWebhookEvent,
    parse_webhook_event,
)

SIGNAL: dict[str, Any] = {
    "id": "sigsub-1",
    "type": "postSearch",
    "label": "lead-1042",
    "status": "active",
    "stoppedReason": None,
    "createdAt": "2026-10-12T10:00:00Z",
    "baselineAt": None,
    "lastCheckedAt": None,
    "nextCheckAt": "2026-10-12T10:20:00Z",
    "term": ["climate tech", "carbon capture"],
    "filter": {"contentType": "videos"},
}
COMMENT_EVENT: dict[str, Any] = {
    "id": "sigev-1",
    "signalId": "sigsub-2",
    "signalType": "postEngagement",
    "label": "launch-post",
    "type": "commentAdded",
    "detectedAt": "2026-10-12T16:40:00Z",
    "postUrl": "https://www.linkedin.com/feed/update/urn:li:activity:1",
    "comment": {
        "commentUrl": "https://www.linkedin.com/feed/update/urn:li:activity:1/?dashCommentUrn=x",
        "author": {"type": "person", "name": "John Doe"},
        "time": "2h",
        "text": "Interested",
        "isReply": True,
        "parentCommentUrn": "urn:li:comment:(activity:1,2)",
    },
}


def test_create_signal_posts_the_target_and_returns_the_signal(
    fake_http_client: FakeHttpClient,
) -> None:
    fake_http_client.queue_response(result=SIGNAL)

    result = LinkedApi(fake_http_client).create_signal(
        CreateSignalParams(
            type="postSearch",
            term=["climate tech", "carbon capture"],
            filter=SignalPostSearchFilter(content_type="videos"),
            label="lead-1042",
        )
    )

    assert fake_http_client.calls == [
        (
            "POST",
            "/signals",
            {
                "type": "postSearch",
                "term": ["climate tech", "carbon capture"],
                "filter": {"contentType": "videos"},
                "label": "lead-1042",
            },
        )
    ]
    assert result.data is not None
    assert result.data.id == "sigsub-1"
    assert result.data.next_check_at == "2026-10-12T10:20:00Z"
    assert result.data.filter == {"contentType": "videos"}


@pytest.mark.parametrize(
    "params, path",
    [
        (None, "/signals"),
        (GetSignalsParams(type="network"), "/signals?type=network"),
        (
            GetSignalsParams(type="postSearch", status="active"),
            "/signals?type=postSearch&status=active",
        ),
    ],
)
def test_get_signals_sends_only_the_filters_given(
    fake_http_client: FakeHttpClient, params: GetSignalsParams | None, path: str
) -> None:
    fake_http_client.queue_response(result={"signals": [SIGNAL]})

    result = LinkedApi(fake_http_client).get_signals(params)

    assert fake_http_client.calls == [("GET", path, None)]
    assert result.data is not None
    assert [signal.id for signal in result.data] == ["sigsub-1"]


@pytest.mark.parametrize(
    "method, verb, path",
    [
        ("get_signal", "GET", "/signals/sigsub-1"),
        ("pause_signal", "POST", "/signals/sigsub-1/pause"),
        ("resume_signal", "POST", "/signals/sigsub-1/resume"),
    ],
)
def test_signal_id_methods_return_the_signal(
    fake_http_client: FakeHttpClient, method: str, verb: str, path: str
) -> None:
    fake_http_client.queue_response(result=SIGNAL)

    result = getattr(LinkedApi(fake_http_client), method)(SignalIdParams(signal_id="sigsub-1"))

    assert fake_http_client.calls == [(verb, path, None)]
    assert result.data.id == "sigsub-1"


def test_delete_signal_quotes_the_id(fake_http_client: FakeHttpClient) -> None:
    fake_http_client.queue_response(result={"deleted": True})

    result = LinkedApi(fake_http_client).delete_signal(SignalIdParams(signal_id="sigsub-a/b"))

    assert fake_http_client.calls == [("DELETE", "/signals/sigsub-a%2Fb", None)]
    assert result.data is True


def test_poll_signals_posts_the_filters_and_parses_event_subjects(
    fake_http_client: FakeHttpClient,
) -> None:
    fake_http_client.queue_response(result={"events": [COMMENT_EVENT]})

    result = LinkedApi(fake_http_client).poll_signals(
        SignalPollRequest(
            since="2026-10-12T00:00:00Z", signal_id="sigsub-2", event_type="commentAdded"
        )
    )

    assert fake_http_client.calls == [
        (
            "POST",
            "/signals/poll",
            {"since": "2026-10-12T00:00:00Z", "signalId": "sigsub-2", "eventType": "commentAdded"},
        )
    ]
    assert result.data is not None
    event = result.data[0]
    assert event.type == "commentAdded"
    assert event.comment is not None
    assert event.comment.parent_comment_urn == "urn:li:comment:(activity:1,2)"


def test_poll_signals_without_request_sends_empty_body(fake_http_client: FakeHttpClient) -> None:
    fake_http_client.queue_response(result={"events": []})

    result = LinkedApi(fake_http_client).poll_signals()

    assert fake_http_client.calls == [("POST", "/signals/poll", {})]
    assert result.data == []


def test_signal_error_from_core_is_raised(fake_http_client: FakeHttpClient) -> None:
    fake_http_client.queue_error(LinkedApiError("signalNotFound", "Signal not found"))

    with pytest.raises(LinkedApiError) as error:
        LinkedApi(fake_http_client).get_signal(SignalIdParams(signal_id="sigsub-1"))

    assert error.value.type == "signalNotFound"


def test_unsuccessful_signal_response_is_raised(fake_http_client: FakeHttpClient) -> None:
    fake_http_client.queue_response(
        success=False,
        error=LinkedApiRequestError(type="signalStopped", message="Delete the stopped signal"),
    )

    with pytest.raises(LinkedApiError) as error:
        LinkedApi(fake_http_client).pause_signal(SignalIdParams(signal_id="sigsub-1"))

    assert error.value.type == "signalStopped"


def test_parse_signal_webhook_event() -> None:
    event = parse_webhook_event(
        json.dumps(
            {
                "id": "sigev-1",
                "type": "signal.commentAdded",
                "createdAt": "2026-10-12T16:40:00.000Z",
                "data": {**COMMENT_EVENT, "accountId": "a1"},
            }
        )
    )

    assert isinstance(event, SignalWebhookEvent)
    assert event.data.account_id == "a1"
    assert event.data.signal_id == "sigsub-2"
    assert event.data.comment is not None
    assert event.data.comment.text == "Interested"


def test_webhook_selection_accepts_signal_events() -> None:
    params = SetWebhookParams(
        url="https://example.test/hook", events=["signal.*", "signal.postFound"]
    )

    assert params.events == ["signal.*", "signal.postFound"]
