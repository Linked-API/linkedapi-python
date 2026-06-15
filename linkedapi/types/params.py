from __future__ import annotations

from linkedapi.types.base import LinkedApiModel


class BaseActionParams(LinkedApiModel):
    pass


class LimitParams(LinkedApiModel):
    limit: int | None = None


class LimitSinceParams(LimitParams):
    since: str | None = None
