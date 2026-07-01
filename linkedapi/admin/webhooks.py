from __future__ import annotations

from typing import Any

from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient
from linkedapi.types.webhooks import (
    DeleteWebhookParams,
    ReplayWebhookDeliveryParams,
    SetWebhookParams,
    SetWebhookPayloadModeParams,
    WebhookDelivery,
    WebhookSubscription,
)


class AdminWebhooks:
    """Manage the client's registered outbound webhook and inspect recent deliveries.

    A client may hold at most one active webhook. It receives every event Linked API emits
    (workflow lifecycle + account status changes); filter by the event ``type`` on your receiver.
    """

    def __init__(self, http_client: HttpClient[Any]) -> None:
        self.http_client = http_client

    def set(self, params: SetWebhookParams) -> WebhookSubscription:
        result = self._post_result("/admin/webhook.set", "Failed to set webhook", params)
        return WebhookSubscription.model_validate(result["webhook"])

    def get(self) -> list[WebhookSubscription]:
        result = self._post_result("/admin/webhook.get", "Failed to get webhooks")
        return [WebhookSubscription.model_validate(item) for item in result["webhooks"]]

    def set_payload_mode(self, params: SetWebhookPayloadModeParams) -> WebhookSubscription:
        result = self._post_result(
            "/admin/webhook.setPayloadMode",
            "Failed to set webhook payload mode",
            params,
        )
        return WebhookSubscription.model_validate(result["webhook"])

    def delete(self, params: DeleteWebhookParams) -> None:
        self._post_void("/admin/webhook.delete", "Failed to delete webhook", params)

    def deliveries(self) -> list[WebhookDelivery]:
        result = self._post_result("/admin/webhook.deliveries", "Failed to get webhook deliveries")
        return [WebhookDelivery.model_validate(item) for item in result["deliveries"]]

    def replay_delivery(self, params: ReplayWebhookDeliveryParams) -> None:
        self._post_void(
            "/admin/webhook.replayDelivery",
            "Failed to replay webhook delivery",
            params,
        )

    def send_test(self) -> None:
        self._post_void("/admin/webhook.sendTest", "Failed to send test webhook")

    def _post_result(
        self,
        path: str,
        default_message: str,
        params: Any | None = None,
    ) -> dict[str, Any]:
        response = self.http_client.post(path, params)
        if response.success and response.result is not None:
            result: dict[str, Any] = response.result
            return result
        raise LinkedApiError(
            response.error.type if response.error else "httpError",
            response.error.message if response.error else default_message,
        )

    def _post_void(self, path: str, default_message: str, params: Any | None = None) -> None:
        response = self.http_client.post(path, params)
        if response.success:
            return
        raise LinkedApiError(
            response.error.type if response.error else "httpError",
            response.error.message if response.error else default_message,
        )
