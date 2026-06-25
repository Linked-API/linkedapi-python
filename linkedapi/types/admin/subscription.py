from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel

SubscriptionStatusValue = Literal["active", "trialing", "past_due", "canceled"]
SeatType = Literal["core", "plus"]
BillingPeriod = Literal["month", "year"]
SetSeatsStatus = Literal["complete", "processing"]


class SubscriptionStatus(LinkedApiModel):
    status: SubscriptionStatusValue | None = None
    eligible_for_trial: bool | None = None
    cancel_at_period_end: bool | None = None


class SubscriptionSeat(LinkedApiModel):
    seat_type: SeatType | None = None
    quantity: int | None = None
    billing_period: BillingPeriod | None = None


class SetSeatsParams(LinkedApiModel):
    quantity: int
    seat_type: SeatType
    billing_period: BillingPeriod


class SetSeatsResult(LinkedApiModel):
    status: SetSeatsStatus | None = None
    payment_link: str | None = None


class SubscriptionSeatsResult(LinkedApiModel):
    seats: list[SubscriptionSeat] | None = None
