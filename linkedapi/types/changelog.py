from __future__ import annotations

from linkedapi.types.base import LinkedApiModel


class ChangelogItem(LinkedApiModel):
    title: str
    body: str
    docs: str


class ChangelogRelease(LinkedApiModel):
    date: str
    items: list[ChangelogItem]


class ChangelogResponse(LinkedApiModel):
    since: str | None
    count: int
    entries: list[ChangelogRelease]
