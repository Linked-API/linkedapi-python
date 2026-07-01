from __future__ import annotations

from typing import Any

from linkedapi.admin.accounts import AdminAccounts
from linkedapi.admin.http_client import AdminHttpClient
from linkedapi.admin.limits import AdminLimits
from linkedapi.admin.subscription import AdminSubscription
from linkedapi.admin.webhooks import AdminWebhooks
from linkedapi.http import HttpClient
from linkedapi.types.admin import AdminConfig


class LinkedApiAdmin:
    """Admin SDK for Linked API subscription, account, limit, and webhook management."""

    def __init__(self, config: AdminConfig | HttpClient[Any]) -> None:
        http_client = (
            config if isinstance(config, HttpClient) else AdminHttpClient(config, config.client)
        )
        self.subscription = AdminSubscription(http_client)
        self.accounts = AdminAccounts(http_client)
        self.limits = AdminLimits(http_client)
        self.webhooks = AdminWebhooks(http_client)
