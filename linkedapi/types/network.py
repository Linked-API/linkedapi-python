from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams

NetworkEventType = Literal[
    "connectionAccepted",
    "connectionAdded",
    "connectionRequestReceived",
]


class SyncNetworkParams(BaseActionParams):
    pass


class NetworkPollRequest(LinkedApiModel):
    since: str | None = None
    type: NetworkEventType | None = None


class NetworkEvent(LinkedApiModel):
    id: str | None = None
    type: NetworkEventType | None = None
    person_url: str | None = None
    detected_at: str | None = None
