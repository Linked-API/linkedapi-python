from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from linkedapi.errors import LinkedApiError
from linkedapi.http import HttpClient
from linkedapi.types.admin import (
    BillingLinkResult,
    CancelResult,
    SetSeatsParams,
    SetSeatsResult,
    SubscriptionPricingResult,
    SubscriptionSeatsResult,
    SubscriptionStatus,
)

TModel = TypeVar("TModel", bound=BaseModel)


class AdminSubscription:
    def __init__(self, http_client: HttpClient[Any]) -> None:
        self.http_client = http_client

    def get_status(self) -> SubscriptionStatus:
        return self._post_result(
            "/admin/subscription.getStatus", SubscriptionStatus, "Failed to get subscription status"
        )

    def get_seats(self) -> SubscriptionSeatsResult:
        return self._post_result(
            "/admin/subscription.getSeats", SubscriptionSeatsResult, "Failed to get seats"
        )

    def get_pricing(self) -> SubscriptionPricingResult:
        return self._post_result(
            "/admin/subscription.getPricing", SubscriptionPricingResult, "Failed to get pricing"
        )

    def set_seats(self, params: SetSeatsParams) -> SetSeatsResult:
        return self._post_result(
            "/admin/subscription.setSeats", SetSeatsResult, "Failed to set seats", params
        )

    def get_billing_link(self) -> BillingLinkResult:
        return self._post_result(
            "/admin/subscription.getBillingLink", BillingLinkResult, "Failed to get billing link"
        )

    def cancel(self) -> CancelResult:
        return self._post_result(
            "/admin/subscription.cancel", CancelResult, "Failed to cancel subscription"
        )

    def _post_result(
        self,
        path: str,
        model: type[TModel],
        default_message: str,
        params: Any | None = None,
    ) -> TModel:
        response = self.http_client.post(path, params)
        if response.success and response.result is not None:
            return model.model_validate(response.result)
        raise LinkedApiError(
            response.error.type if response.error else "httpError",
            response.error.message if response.error else default_message,
        )
