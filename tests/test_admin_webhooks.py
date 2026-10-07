from __future__ import annotations

from typing import Any

import pytest
import requests_mock
from pydantic import ValidationError

from linkedapi import (
    AdminConfig,
    AdminHttpClient,
    DeleteWebhookHeaderParams,
    LinkedApiAdmin,
    LinkedApiModel,
    RevealWebhookSecretParams,
    RotateWebhookSecretParams,
    SetWebhookEventsParams,
    SetWebhookHeaderParams,
    SetWebhookHeadersParams,
    SetWebhookParams,
    SetWebhookSigningParams,
    WebhookSubscription,
)

BASE_URL = "https://api.test"
WEBHOOK: dict[str, Any] = {
    "id": "w1",
    "url": "https://receiver.test",
    "payloadMode": "fat",
    "isActive": True,
    "createdAt": "2026-10-07T00:00:00Z",
    "signingEnabled": True,
    "headerNames": ["x-receiver"],
    "events": None,
}


@pytest.mark.parametrize(
    ("method", "route", "params", "expected"),
    [
        (
            "set_signing",
            "setSigning",
            SetWebhookSigningParams(id="w1", signing_enabled=True),
            {"id": "w1", "signingEnabled": True},
        ),
        (
            "set_signing",
            "setSigning",
            SetWebhookSigningParams(id="w1", signing_enabled=False),
            {"id": "w1", "signingEnabled": False},
        ),
        (
            "set_headers",
            "setHeaders",
            SetWebhookHeadersParams(id="w1", headers=None),
            {"id": "w1", "headers": None},
        ),
        (
            "set_headers",
            "setHeaders",
            SetWebhookHeadersParams(id="w1", headers={}),
            {"id": "w1", "headers": {}},
        ),
        (
            "set_headers",
            "setHeaders",
            SetWebhookHeadersParams(id="w1", headers={"x-receiver": "value"}),
            {"id": "w1", "headers": {"x-receiver": "value"}},
        ),
        (
            "set_header",
            "setHeader",
            SetWebhookHeaderParams(id="w1", name="X-Receiver", value="value"),
            {"id": "w1", "name": "X-Receiver", "value": "value"},
        ),
        (
            "delete_header",
            "deleteHeader",
            DeleteWebhookHeaderParams(id="w1", name="X-Receiver"),
            {"id": "w1", "name": "X-Receiver"},
        ),
        ("reveal_secret", "revealSecret", RevealWebhookSecretParams(id="w1"), {"id": "w1"}),
        ("rotate_secret", "rotateSecret", RotateWebhookSecretParams(id="w1"), {"id": "w1"}),
        (
            "set_events",
            "setEvents",
            SetWebhookEventsParams(id="w1", events=None),
            {"id": "w1", "events": None},
        ),
        (
            "set_events",
            "setEvents",
            SetWebhookEventsParams(id="w1", events=["workflow.*", "account.active"]),
            {"id": "w1", "events": ["workflow.*", "account.active"]},
        ),
    ],
)
def test_management_json_contract(
    requests_mock: requests_mock.Mocker,
    method: str,
    route: str,
    params: LinkedApiModel,
    expected: dict[str, Any],
) -> None:
    webhook = (
        WEBHOOK | {"secret": "stored-secret"}
        if method in ["reveal_secret", "rotate_secret"]
        else WEBHOOK
    )
    requests_mock.post(
        f"{BASE_URL}/admin/webhook.{route}", json={"success": True, "result": {"webhook": webhook}}
    )
    admin = LinkedApiAdmin(AdminHttpClient(AdminConfig(linked_api_token="lat"), base_url=BASE_URL))
    result = getattr(admin.webhooks, method)(params)
    request = requests_mock.last_request
    assert request is not None
    assert request.method == "POST"
    assert request.url == f"{BASE_URL}/admin/webhook.{route}"
    assert request.json() == expected
    assert isinstance(result, WebhookSubscription)
    assert result.signing_enabled is True
    assert result.header_names == ["x-receiver"]
    assert result.events is None
    assert result.secret == webhook.get("secret")


def test_event_types_has_no_body_and_preserves_server_order(
    requests_mock: requests_mock.Mocker,
) -> None:
    event_types = ["network.connectionAccepted", "workflow.created", "inbox.messageSent"]
    requests_mock.post(
        f"{BASE_URL}/admin/webhook.eventTypes",
        json={"success": True, "result": {"eventTypes": event_types}},
    )
    admin = LinkedApiAdmin(AdminHttpClient(AdminConfig(linked_api_token="lat"), base_url=BASE_URL))
    assert admin.webhooks.event_types() == event_types
    request = requests_mock.last_request
    assert request is not None
    assert request.method == "POST"
    assert request.body is None


@pytest.mark.parametrize(
    "params",
    [
        SetWebhookParams(url="https://receiver.test"),
        SetWebhookParams(
            url="https://receiver.test", events=None, signing_enabled=None, headers=None
        ),
    ],
)
def test_set_omits_optional_none_fields(
    requests_mock: requests_mock.Mocker, params: SetWebhookParams
) -> None:
    requests_mock.post(
        f"{BASE_URL}/admin/webhook.set", json={"success": True, "result": {"webhook": WEBHOOK}}
    )
    admin = LinkedApiAdmin(AdminHttpClient(AdminConfig(linked_api_token="lat"), base_url=BASE_URL))
    admin.webhooks.set(params)
    request = requests_mock.last_request
    assert request is not None
    assert request.json() == {"url": "https://receiver.test"}


def test_set_optional_fields_and_secret_response(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.post(
        f"{BASE_URL}/admin/webhook.set",
        json={"success": True, "result": {"webhook": WEBHOOK | {"secret": "stored-secret"}}},
    )
    admin = LinkedApiAdmin(AdminHttpClient(AdminConfig(linked_api_token="lat"), base_url=BASE_URL))
    result = admin.webhooks.set(
        SetWebhookParams(
            url="https://receiver.test",
            payload_mode="fat",
            signing_enabled=True,
            headers={"x-receiver": "value"},
            events=["inbox.*"],
        )
    )
    request = requests_mock.last_request
    assert request is not None
    assert request.json() == {
        "url": "https://receiver.test",
        "payloadMode": "fat",
        "signingEnabled": True,
        "headers": {"x-receiver": "value"},
        "events": ["inbox.*"],
    }
    assert result.secret == "stored-secret"


def test_subscription_camel_case_fields() -> None:
    subscription = WebhookSubscription.model_validate(
        WEBHOOK | {"events": ["workflow.*"], "secret": "stored-secret"}
    )
    assert subscription.signing_enabled is True
    assert subscription.header_names == ["x-receiver"]
    assert subscription.events == ["workflow.*"]
    assert subscription.secret == "stored-secret"


@pytest.mark.parametrize("events", [["workflow.completed", "billing.invoicePaid"], ["billing.*"]])
def test_get_preserves_new_event_selectors(
    requests_mock: requests_mock.Mocker, events: list[str]
) -> None:
    requests_mock.post(
        f"{BASE_URL}/admin/webhook.get",
        json={"success": True, "result": {"webhooks": [WEBHOOK | {"events": events}]}},
    )
    admin = LinkedApiAdmin(AdminHttpClient(AdminConfig(linked_api_token="lat"), base_url=BASE_URL))
    subscriptions = admin.webhooks.get()
    assert len(subscriptions) == 1
    assert isinstance(subscriptions[0], WebhookSubscription)
    assert subscriptions[0].events == events


def test_deliveries_preserves_new_event_types(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.post(
        f"{BASE_URL}/admin/webhook.deliveries",
        json={
            "success": True,
            "result": {
                "deliveries": [
                    {"id": "d1", "eventType": "workflow.completed"},
                    {"id": "d2", "eventType": "post.commentReceived"},
                ]
            },
        },
    )
    admin = LinkedApiAdmin(AdminHttpClient(AdminConfig(linked_api_token="lat"), base_url=BASE_URL))
    deliveries = admin.webhooks.deliveries()
    assert [delivery.event_type for delivery in deliveries] == [
        "workflow.completed",
        "post.commentReceived",
    ]


def test_test_event_cannot_be_selected() -> None:
    with pytest.raises(ValidationError):
        SetWebhookEventsParams.model_validate({"id": "w1", "events": ["webhook.test"]})
