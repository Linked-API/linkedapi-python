from __future__ import annotations

import json

from linkedapi.types.webhooks import (
    AccountWebhookEvent,
    MessageWebhookEvent,
    NetworkWebhookEvent,
    WebhookEvent,
    WebhookTestEvent,
    WorkflowWebhookEvent,
)


def parse_webhook_event(raw_body: str | bytes) -> WebhookEvent:
    """Parse a raw webhook request body into a typed Linked API event.

    Pass the raw HTTP body (``str`` or ``bytes``) exactly as received, then branch on the
    returned event's ``type``.

    Raises:
        ValueError: when the body is not valid JSON or is missing the ``id`` / ``type`` fields,
            or carries an unknown event type.
    """
    text = raw_body.decode("utf-8") if isinstance(raw_body, (bytes, bytearray)) else raw_body

    try:
        parsed = json.loads(text)
    except (ValueError, TypeError) as error:
        msg = "Invalid webhook payload: body is not valid JSON"
        raise ValueError(msg) from error

    if (
        not isinstance(parsed, dict)
        or not isinstance(parsed.get("id"), str)
        or not isinstance(parsed.get("type"), str)
    ):
        msg = 'Invalid webhook payload: missing "id" or "type"'
        raise ValueError(msg)

    event_type: str = parsed["type"]
    if event_type.startswith("workflow."):
        return WorkflowWebhookEvent.model_validate(parsed)
    if event_type.startswith("account."):
        return AccountWebhookEvent.model_validate(parsed)
    if event_type.startswith("inbox."):
        return MessageWebhookEvent.model_validate(parsed)
    if event_type.startswith("network."):
        return NetworkWebhookEvent.model_validate(parsed)
    if event_type == "webhook.test":
        return WebhookTestEvent.model_validate(parsed)

    msg = f"Unknown webhook event type: {event_type}"
    raise ValueError(msg)
