from __future__ import annotations

from typing import Any, Literal

from pydantic import SerializerFunctionWrapHandler, model_serializer

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.message import ConversationType, MessageSender

WebhookPayloadMode = Literal["thin", "fat"]
WebhookEventType = Literal[
    "workflow.created",
    "workflow.started",
    "workflow.completed",
    "account.active",
    "account.reconnectionRequired",
    "account.frozen",
    "account.deleted",
    "inbox.messageReceived",
    "inbox.messageSent",
    "network.connectionAccepted",
    "network.connectionAdded",
    "network.connectionRequestReceived",
    "webhook.test",
]
WebhookEventSelector = Literal[
    "workflow.created",
    "workflow.started",
    "workflow.completed",
    "account.active",
    "account.reconnectionRequired",
    "account.frozen",
    "account.deleted",
    "inbox.messageReceived",
    "inbox.messageSent",
    "network.connectionAccepted",
    "network.connectionAdded",
    "network.connectionRequestReceived",
    "workflow.*",
    "account.*",
    "inbox.*",
    "network.*",
]
WebhookDeliveryStatus = Literal["pending", "delivering", "success", "failed"]
WorkflowWebhookStatus = Literal["pending", "running", "completed", "failed"]
AccountWebhookStatus = Literal["active", "reconnection_required", "frozen", "deleted"]


class WebhookSubscription(LinkedApiModel):
    id: str | None = None
    url: str | None = None
    payload_mode: WebhookPayloadMode | None = None
    is_active: bool | None = None
    signing_enabled: bool | None = None
    header_names: list[str] | None = None
    events: list[str] | None = None
    # Returned only by set with signing on, set_signing(True), reveal_secret or rotate_secret.
    secret: str | None = None
    created_at: str | None = None


class WebhookDelivery(LinkedApiModel):
    id: str | None = None
    event_type: str | None = None
    event_id: str | None = None
    status: WebhookDeliveryStatus | None = None
    attempts: int | None = None
    response_status_code: int | None = None
    last_error: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class SetWebhookParams(LinkedApiModel):
    url: str
    payload_mode: WebhookPayloadMode | None = None
    signing_enabled: bool | None = None
    headers: dict[str, str] | None = None
    events: list[WebhookEventSelector] | None = None


class SetWebhookPayloadModeParams(LinkedApiModel):
    id: str
    payload_mode: WebhookPayloadMode


class SetWebhookSigningParams(LinkedApiModel):
    id: str
    signing_enabled: bool


class SetWebhookHeadersParams(LinkedApiModel):
    id: str
    headers: dict[str, str] | None

    @model_serializer(mode="wrap")
    def _serialize(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        result: dict[str, Any] = handler(self)
        # Core requires explicit null to clear headers, even when requests exclude None.
        if self.headers is None:
            result["headers"] = None
        return result


class SetWebhookHeaderParams(LinkedApiModel):
    id: str
    name: str
    value: str


class DeleteWebhookHeaderParams(LinkedApiModel):
    id: str
    name: str


class RevealWebhookSecretParams(LinkedApiModel):
    id: str


class RotateWebhookSecretParams(LinkedApiModel):
    id: str


class SetWebhookEventsParams(LinkedApiModel):
    id: str
    events: list[WebhookEventSelector] | None

    @model_serializer(mode="wrap")
    def _serialize(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        result: dict[str, Any] = handler(self)
        # Core requires explicit null to select all events, even when requests exclude None.
        if self.events is None:
            result["events"] = None
        return result


class DeleteWebhookParams(LinkedApiModel):
    id: str


class ReplayWebhookDeliveryParams(LinkedApiModel):
    delivery_id: str


class WorkflowWebhookEventData(LinkedApiModel):
    workflow_id: str | None = None
    account_id: str | None = None
    status: WorkflowWebhookStatus | None = None
    # Present only on workflow.completed delivered in `fat` payload mode; in `thin` mode fetch the
    # result via the workflow API by workflow_id.
    result: Any | None = None


class WorkflowWebhookEvent(LinkedApiModel):
    id: str
    type: Literal["workflow.created", "workflow.started", "workflow.completed"]
    created_at: str | None = None
    data: WorkflowWebhookEventData


class AccountWebhookEventData(LinkedApiModel):
    account_id: str | None = None
    status: AccountWebhookStatus | None = None


class AccountWebhookEvent(LinkedApiModel):
    id: str
    type: Literal[
        "account.active",
        "account.reconnectionRequired",
        "account.frozen",
        "account.deleted",
    ]
    created_at: str | None = None
    data: AccountWebhookEventData


class MessageWebhookEventData(LinkedApiModel):
    account_id: str | None = None
    type: ConversationType | None = None
    thread_id: str | None = None
    person_urn: str | None = None
    person_hashed_url: str | None = None
    person_public_url: str | None = None
    # Deprecated: use person_hashed_url. Still returned by the API for compatibility.
    person_url: str | None = None
    message_id: str | None = None
    sender: MessageSender | None = None
    text: str | None = None
    time: str | None = None


class MessageWebhookEvent(LinkedApiModel):
    id: str
    type: Literal["inbox.messageReceived", "inbox.messageSent"]
    created_at: str | None = None
    data: MessageWebhookEventData


class NetworkWebhookEventData(LinkedApiModel):
    account_id: str | None = None
    person_urn: str | None = None
    person_url: str | None = None
    detected_at: str | None = None


class NetworkWebhookEvent(LinkedApiModel):
    id: str
    type: Literal[
        "network.connectionAccepted",
        "network.connectionAdded",
        "network.connectionRequestReceived",
    ]
    created_at: str | None = None
    data: NetworkWebhookEventData


class WebhookTestEventData(LinkedApiModel):
    message: str | None = None


class WebhookTestEvent(LinkedApiModel):
    id: str
    type: Literal["webhook.test"]
    created_at: str | None = None
    data: WebhookTestEventData


WebhookEvent = (
    WorkflowWebhookEvent
    | AccountWebhookEvent
    | MessageWebhookEvent
    | NetworkWebhookEvent
    | WebhookTestEvent
)
