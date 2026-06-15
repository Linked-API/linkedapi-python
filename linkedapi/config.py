from __future__ import annotations

from linkedapi.types.base import LinkedApiModel


class LinkedApiConfig(LinkedApiModel):
    linked_api_token: str
    identification_token: str
    client: str = "python"
    base_url: str = "https://api.linkedapi.io"
