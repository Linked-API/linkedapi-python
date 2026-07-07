from __future__ import annotations

from typing import Literal

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams

ConversationType = Literal["st", "nv"]
MessageSender = Literal["us", "them"]


class SendMessageParams(BaseActionParams):
    text: str
    person_url: str | None = None
    thread_id: str | None = None


class SyncConversationParams(BaseActionParams):
    person_url: str


class SyncInboxParams(BaseActionParams):
    pass


class ManageConversationParams(BaseActionParams):
    thread_id: str
    operation: str


class NvSendMessageParams(BaseActionParams):
    text: str
    person_url: str | None = None
    subject: str | None = None
    thread_id: str | None = None


class NvSyncConversationParams(BaseActionParams):
    person_url: str


class NvSyncInboxParams(BaseActionParams):
    pass


class NvManageConversationParams(BaseActionParams):
    thread_id: str
    operation: str


class ConversationPollRequest(LinkedApiModel):
    person_url: str
    type: ConversationType
    since: str | None = None


class Message(LinkedApiModel):
    id: str | None = None
    sender: MessageSender | None = None
    text: str | None = None
    time: str | None = None
    thread_id: str | None = None


class ConversationPollResult(LinkedApiModel):
    person_url: str | None = None
    type: ConversationType | None = None
    messages: list[Message] | None = None
    since: str | None = None


class InboxPollRequest(LinkedApiModel):
    since: str | None = None
    type: ConversationType | None = None
    thread_id: str | None = None


class InboxMessage(LinkedApiModel):
    id: str | None = None
    type: ConversationType | None = None
    thread_id: str | None = None
    person_url: str | None = None
    sender: MessageSender | None = None
    text: str | None = None
    time: str | None = None
