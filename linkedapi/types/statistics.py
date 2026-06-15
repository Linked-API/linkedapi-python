from __future__ import annotations

from linkedapi.types.base import LinkedApiModel


class RetrieveSSIResult(LinkedApiModel):
    ssi: int | None = None
    industry_top: int | None = None
    network_top: int | None = None


class RetrievePerformanceResult(LinkedApiModel):
    followers_count: int | None = None
    post_views_last_7_days: int | None = None
    profile_views_last_90_days: int | None = None
    search_appearances_previous_week: int | None = None


class ApiUsageParams(LinkedApiModel):
    start: str
    end: str


class ApiUsageAction(LinkedApiModel):
    action_type: str | None = None
    success: bool | None = None
    time: str | None = None
