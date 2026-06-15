from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams

ConversationType = Literal["st", "nv"]
MessageSender = Literal["us", "them"]


class SendMessageParams(BaseActionParams):
    person_url: str
    text: str


class SyncConversationParams(BaseActionParams):
    person_url: str


class NvSendMessageParams(BaseActionParams):
    person_url: str
    text: str
    subject: str


class NvSyncConversationParams(BaseActionParams):
    person_url: str


class ConversationPollRequest(LinkedApiModel):
    person_url: str
    type: ConversationType
    since: str | None = None


class Message(LinkedApiModel):
    id: str | None = None
    sender: MessageSender | None = None
    text: str | None = None
    time: str | None = None


class ConversationPollResult(LinkedApiModel):
    person_url: str | None = None
    type: ConversationType | None = None
    messages: list[Message] | None = None
    since: str | None = None
