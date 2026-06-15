from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel

SubscriptionStatusValue = Literal["active", "trialing", "past_due", "canceled"]
SeatType = Literal["core", "plus"]
BillingPeriod = Literal["month", "year"]
Currency = Literal["usd", "eur"]
SetSeatsStatus = Literal["complete", "processing"]


class SubscriptionStatus(LinkedApiModel):
    status: SubscriptionStatusValue | None = None
    eligible_for_trial: bool | None = None
    cancel_at_period_end: bool | None = None


class SubscriptionSeat(LinkedApiModel):
    seat_type: SeatType | None = None
    quantity: int | None = None
    billing_period: BillingPeriod | None = None


class SubscriptionProduct(LinkedApiModel):
    id: str | None = None
    seat_type: SeatType | None = None
    billing_period: BillingPeriod | None = None
    unit_price: int | None = None
    currency: Currency | None = None


class SetSeatsParams(LinkedApiModel):
    quantity: int
    seat_type: SeatType
    billing_period: BillingPeriod


class SetSeatsResult(LinkedApiModel):
    status: SetSeatsStatus | None = None
    payment_link: str | None = None


class BillingLinkResult(LinkedApiModel):
    stripe_link: str | None = None


class CancelResult(LinkedApiModel):
    cancel_at_date: str | None = None


class SubscriptionSeatsResult(LinkedApiModel):
    seats: list[SubscriptionSeat] | None = None


class SubscriptionPricingResult(LinkedApiModel):
    products: list[SubscriptionProduct] | None = None
