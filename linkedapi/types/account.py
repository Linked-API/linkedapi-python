from __future__ import annotations

from linkedapi.types.base import LinkedApiModel


class AccountInfo(LinkedApiModel):
    name: str | None = None
    url: str | None = None
