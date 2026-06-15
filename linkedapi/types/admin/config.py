from __future__ import annotations

from linkedapi.types.base import LinkedApiModel


class AdminConfig(LinkedApiModel):
    linked_api_token: str
    client: str = "python"
