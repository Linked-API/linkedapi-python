from __future__ import annotations

from typing import Any

import requests_mock

from linkedapi import (
    AdminConfig,
    AdminHttpClient,
    CancelConnectionSessionParams,
    CreateReconnectionSessionParams,
    DeleteLimitEntry,
    DeleteLimitsParams,
    DisconnectParams,
    GetConnectionSessionParams,
    GetLimitsParams,
    GetLimitsUsageParams,
    LinkedApiAdmin,
    RegenerateTokenParams,
    ReparseAccountInfoParams,
    ResetLimitsParams,
    SetLimitEntry,
    SetLimitsParams,
    SetSeatsParams,
)


def test_admin_http_client_omits_identification_token(
    requests_mock: requests_mock.Mocker,
) -> None:
    requests_mock.post(
        "https://api.test/admin/subscription.getStatus",
        json={
            "success": True,
            "result": {
                "status": "active",
                "eligibleForTrial": False,
                "cancelAtPeriodEnd": False,
            },
        },
    )
    http_client = AdminHttpClient(AdminConfig(linked_api_token="lat"), base_url="https://api.test")
    admin = LinkedApiAdmin(http_client)

    status = admin.subscription.get_status()

    request = requests_mock.last_request
    assert status.status == "active"
    assert request is not None
    assert request.headers["linked-api-token"] == "lat"
    assert request.headers["client"] == "python"
    assert "identification-token" not in request.headers


def test_admin_methods_use_node_paths(requests_mock: requests_mock.Mocker) -> None:
    base_url = "https://api.test"
    admin = LinkedApiAdmin(AdminHttpClient(AdminConfig(linked_api_token="lat"), base_url=base_url))
    paths_and_results: list[tuple[str, dict[str, Any] | None]] = [
        (
            "/admin/subscription.getStatus",
            {"status": "active", "eligibleForTrial": False, "cancelAtPeriodEnd": False},
        ),
        ("/admin/subscription.getSeats", {"seats": []}),
        ("/admin/subscription.setSeats", {"status": "complete"}),
        ("/admin/accounts.getAll", {"accounts": [], "pendingConnectionSessions": []}),
        ("/admin/accounts.disconnect", None),
        ("/admin/accounts.reparseAccountInfo", {"workflowId": "workflow-1"}),
        ("/admin/accounts.regenerateIdentificationToken", {"token": "new"}),
        ("/admin/accounts.createConnectionSession", {"sessionId": "s1", "connectionLink": "u"}),
        (
            "/admin/accounts.createReconnectionSession",
            {"reconnectionSessionId": "s2", "reconnectionLink": "u2"},
        ),
        (
            "/admin/accounts.getConnectionSession",
            {"session": {"sessionId": "s1", "status": "pending", "type": "connect"}},
        ),
        ("/admin/accounts.cancelConnectionSession", None),
        ("/admin/limits.getDefaults", {"limits": []}),
        ("/admin/limits.get", {"limits": []}),
        ("/admin/limits.getUsage", {"usage": []}),
        ("/admin/limits.set", None),
        ("/admin/limits.delete", None),
        ("/admin/limits.resetToDefaults", None),
    ]
    for path, result in paths_and_results:
        payload: dict[str, Any] = {"success": True}
        if result is not None:
            payload["result"] = result
        requests_mock.post(f"{base_url}{path}", json=payload)

    admin.subscription.get_status()
    admin.subscription.get_seats()
    admin.subscription.set_seats(
        SetSeatsParams(quantity=1, seat_type="core", billing_period="month")
    )
    admin.accounts.get_all()
    admin.accounts.disconnect(DisconnectParams(account_id="a1"))
    admin.accounts.reparse_account_info(ReparseAccountInfoParams(account_id="a1"))
    admin.accounts.regenerate_identification_token(RegenerateTokenParams(account_id="a1"))
    admin.accounts.create_connection_session()
    admin.accounts.create_reconnection_session(CreateReconnectionSessionParams(account_id="a1"))
    admin.accounts.get_connection_session(GetConnectionSessionParams(session_id="s1"))
    admin.accounts.cancel_connection_session(CancelConnectionSessionParams(session_id="s1"))
    admin.limits.get_defaults()
    admin.limits.get(GetLimitsParams(account_id="a1"))
    admin.limits.get_usage(GetLimitsUsageParams(account_id="a1"))
    admin.limits.set(
        SetLimitsParams(
            account_id="a1",
            limits=[
                SetLimitEntry(
                    category="stMessages",
                    period="daily",
                    max_value=10,
                )
            ],
        )
    )
    admin.limits.delete(
        DeleteLimitsParams(
            account_id="a1",
            limits=[DeleteLimitEntry(category="stMessages", period="daily")],
        )
    )
    admin.limits.reset_to_defaults(ResetLimitsParams(account_id="a1"))

    assert [request.url.removeprefix(base_url) for request in requests_mock.request_history] == [
        path for path, _ in paths_and_results
    ]
