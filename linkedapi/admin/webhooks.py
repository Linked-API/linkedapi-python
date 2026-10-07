from __future__ import annotations

from typing import Any

from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient
from linkedapi.types.webhooks import (
    DeleteWebhookHeaderParams,
    DeleteWebhookParams,
    ReplayWebhookDeliveryParams,
    RevealWebhookSecretParams,
    RotateWebhookSecretParams,
    SetWebhookEventsParams,
    SetWebhookHeaderParams,
    SetWebhookHeadersParams,
    SetWebhookParams,
    SetWebhookPayloadModeParams,
    SetWebhookSigningParams,
    WebhookDelivery,
    WebhookSubscription,
)


class AdminWebhooks:
    """Manage the client's registered outbound webhook and inspect recent deliveries.

    A client may hold at most one active webhook. Its event selectors control which workflow,
    account, inbox and network events it receives; None selects all events. Test events are
    always delivered. Signing and custom headers are configured per subscription.
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

    def set_signing(self, params: SetWebhookSigningParams) -> WebhookSubscription:
        """Enable or disable signing. Enabling returns the stored secret."""
        result = self._post_result(
            "/admin/webhook.setSigning",
            "Failed to set webhook signing",
            params,
        )
        return WebhookSubscription.model_validate(result["webhook"])

    def set_headers(self, params: SetWebhookHeadersParams) -> WebhookSubscription:
        """Replace all custom headers. None or an empty dict clears them."""
        result = self._post_result(
            "/admin/webhook.setHeaders",
            "Failed to set webhook headers",
            params,
        )
        return WebhookSubscription.model_validate(result["webhook"])

    def set_header(self, params: SetWebhookHeaderParams) -> WebhookSubscription:
        """Set one custom header; its name is matched case-insensitively."""
        result = self._post_result(
            "/admin/webhook.setHeader",
            "Failed to set webhook header",
            params,
        )
        return WebhookSubscription.model_validate(result["webhook"])

    def delete_header(self, params: DeleteWebhookHeaderParams) -> WebhookSubscription:
        """Remove one custom header; its name is matched case-insensitively."""
        result = self._post_result(
            "/admin/webhook.deleteHeader",
            "Failed to delete webhook header",
            params,
        )
        return WebhookSubscription.model_validate(result["webhook"])

    def reveal_secret(self, params: RevealWebhookSecretParams) -> WebhookSubscription:
        """Return the current signing secret without changing it."""
        result = self._post_result(
            "/admin/webhook.revealSecret",
            "Failed to reveal webhook secret",
            params,
        )
        return WebhookSubscription.model_validate(result["webhook"])

    def rotate_secret(self, params: RotateWebhookSecretParams) -> WebhookSubscription:
        """Replace the signing secret and return its new value."""
        result = self._post_result(
            "/admin/webhook.rotateSecret",
            "Failed to rotate webhook secret",
            params,
        )
        return WebhookSubscription.model_validate(result["webhook"])

    def set_events(self, params: SetWebhookEventsParams) -> WebhookSubscription:
        """Select event types or namespace wildcards; None selects all. Tests always deliver."""
        result = self._post_result(
            "/admin/webhook.setEvents",
            "Failed to set webhook events",
            params,
        )
        return WebhookSubscription.model_validate(result["webhook"])

    def event_types(self) -> list[str]:
        """Return selectable event types in the server's order.

        The catalog excludes webhook.test, which is always delivered.
        """
        result = self._post_result("/admin/webhook.eventTypes", "Failed to get webhook event types")
        event_types: list[str] = result["eventTypes"]
        return event_types

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
