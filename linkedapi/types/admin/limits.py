from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel

LimitCategory = Literal[
    "stPersonProfileViews",
    "stCompanyPageViews",
    "stConnectionRequests",
    "stMessages",
    "stSearchQueries",
    "stReactions",
    "stComments",
    "stPosts",
    "nvPersonProfileViews",
    "nvCompanyPageViews",
    "nvMessages",
]
LimitPeriod = Literal["daily", "weekly", "monthly"]


class Limit(LinkedApiModel):
    category: LimitCategory | None = None
    period: LimitPeriod | None = None
    max_value: int | None = None
    is_enabled: bool | None = None


class LimitUsage(LinkedApiModel):
    category: LimitCategory | None = None
    period: LimitPeriod | None = None
    max_value: int | None = None
    current_usage: int | None = None
    is_enabled: bool | None = None


class GetLimitsParams(LinkedApiModel):
    account_id: str


class GetLimitsUsageParams(LinkedApiModel):
    account_id: str


class SetLimitEntry(LinkedApiModel):
    category: LimitCategory
    period: LimitPeriod
    max_value: int
    is_enabled: bool | None = None


class SetLimitsParams(LinkedApiModel):
    account_id: str
    limits: list[SetLimitEntry]


class DeleteLimitEntry(LinkedApiModel):
    category: LimitCategory
    period: LimitPeriod


class DeleteLimitsParams(LinkedApiModel):
    account_id: str
    limits: list[DeleteLimitEntry]


class ResetLimitsParams(LinkedApiModel):
    account_id: str


class LimitsResult(LinkedApiModel):
    limits: list[Limit] | None = None


class LimitUsageResult(LinkedApiModel):
    usage: list[LimitUsage] | None = None
