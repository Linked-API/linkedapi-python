from __future__ import annotations

import json

from linkedapi import (
    AccountWebhookEvent,
    MessageWebhookEvent,
    UnknownWebhookEvent,
    WorkflowWebhookEvent,
    parse_webhook_event,
)


def test_parse_workflow_event() -> None:
    event = parse_webhook_event(
        json.dumps(
            {
                "id": "e1",
                "type": "workflow.completed",
                "data": {"workflowId": "wf1", "accountId": "a1", "status": "completed"},
            }
        )
    )

    assert isinstance(event, WorkflowWebhookEvent)
    assert event.data.workflow_id == "wf1"


def test_parse_account_event() -> None:
    event = parse_webhook_event(
        json.dumps({"id": "e2", "type": "account.frozen", "data": {"accountId": "a1"}})
    )

    assert isinstance(event, AccountWebhookEvent)
    assert event.data.account_id == "a1"


def test_parse_message_received_event() -> None:
    event = parse_webhook_event(
        json.dumps(
            {
                "id": "e3",
                "type": "inbox.messageReceived",
                "data": {
                    "accountId": "a1",
                    "type": "st",
                    "threadId": "t1",
                    "personUrl": "u",
                    "messageId": "m1",
                    "sender": "them",
                    "text": "hello",
                    "time": "now",
                },
            }
        )
    )

    assert isinstance(event, MessageWebhookEvent)
    assert event.type == "inbox.messageReceived"
    assert event.data.thread_id == "t1"
    assert event.data.message_id == "m1"
    assert event.data.sender == "them"


def test_parse_message_sent_event() -> None:
    event = parse_webhook_event(
        json.dumps(
            {
                "id": "e4",
                "type": "inbox.messageSent",
                "data": {"accountId": "a1", "type": "nv", "sender": "us", "text": "hi"},
            }
        )
    )

    assert isinstance(event, MessageWebhookEvent)
    assert event.type == "inbox.messageSent"
    assert event.data.type == "nv"


def test_parse_unknown_event_keeps_type_and_payload() -> None:
    event = parse_webhook_event(
        json.dumps({"id": "e5", "type": "unknown.thing", "data": {"future": "value"}})
    )

    assert isinstance(event, UnknownWebhookEvent)
    assert event.type == "unknown.thing"
    assert event.data == {"future": "value"}
