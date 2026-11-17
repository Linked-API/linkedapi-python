from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.post import PostAuthor, PostComment, ReactionType
from linkedapi.types.profile_viewers import ProfileViewer
from linkedapi.types.search_posts import (
    PostSearchContentType,
    PostSearchPostedBy,
    SearchPostResult,
    SearchPostsCompanyFilterEntry,
    SearchPostsPersonFilterEntry,
)

SignalType = Literal[
    "personPosts",
    "companyPosts",
    "postSearch",
    "postEngagement",
    "network",
    "profileViewers",
]
SignalStatus = Literal["active", "paused", "stopped"]
SignalStoppedReason = Literal["targetNotFound", "watchPeriodEnded"]
SignalEventType = Literal[
    "postPublished",
    "postFound",
    "commentAdded",
    "reactionAdded",
    "profileViewed",
    "connectionAccepted",
    "connectionAdded",
    "connectionRequestReceived",
]


class SignalPostSearchFilter(LinkedApiModel):
    """The filters a "postSearch" signal accepts: the content search filters other than sort,
    date and author."""

    content_type: PostSearchContentType | None = None
    posted_by: list[PostSearchPostedBy] | None = None
    mentioning_members: list[SearchPostsPersonFilterEntry] | None = None
    mentioning_companies: list[SearchPostsCompanyFilterEntry] | None = None
    author_companies: list[SearchPostsCompanyFilterEntry] | None = None
    author_industries: list[str] | None = None


class CreateSignalParams(LinkedApiModel):
    """A signal to create. The "type" decides the target field.

    "personPosts" takes "person_url", "companyPosts" takes "company_url", "postSearch" takes
    "term" (a phrase or a list of up to three) and an optional "filter", "postEngagement" takes
    "post_url" or "my_posts=True", and "network" and "profileViewers" take none. "label" is your
    own identifier, up to 64 characters, returned with the signal and every event it produces.
    """

    type: SignalType
    label: str | None = Field(default=None, max_length=64)
    person_url: str | None = None
    company_url: str | None = None
    post_url: str | None = None
    my_posts: Literal[True] | None = None
    term: str | list[str] | None = None
    filter: SignalPostSearchFilter | None = None


class GetSignalsParams(LinkedApiModel):
    type: SignalType | None = None
    status: SignalStatus | None = None


class SignalIdParams(LinkedApiModel):
    signal_id: str


class SignalPollRequest(LinkedApiModel):
    """Pass "since" as the "detected_at" of the newest event you have; without it every
    retained event is returned."""

    since: str | None = None
    signal_id: str | None = None
    signal_type: SignalType | None = None
    event_type: SignalEventType | None = None


class Signal(LinkedApiModel):
    id: str | None = None
    type: SignalType | str | None = None
    label: str | None = None
    status: SignalStatus | str | None = None
    # Why Linked API stopped the signal; None unless status is "stopped".
    stopped_reason: SignalStoppedReason | str | None = None
    created_at: str | None = None
    baseline_at: str | None = None
    last_checked_at: str | None = None
    next_check_at: str | None = None
    person_url: str | None = None
    company_url: str | None = None
    post_url: str | None = None
    my_posts: bool | None = None
    term: str | list[str] | None = None
    filter: dict[str, Any] | None = None


class SignalComment(PostComment):
    parent_comment_urn: str | None = None


class SignalReaction(LinkedApiModel):
    actor: PostAuthor | None = None
    type: ReactionType | str | None = None


class SignalEvent(LinkedApiModel):
    """One event a signal detected. Which subject fields are set depends on "type": "post" for
    postPublished and postFound, "post_url" with "comment" or "reaction", "viewer" for
    profileViewed, and "person_urn" with "person_url" for the connection events."""

    id: str | None = None
    signal_id: str | None = None
    signal_type: SignalType | str | None = None
    label: str | None = None
    type: SignalEventType | str | None = None
    # When Linked API recorded the event, not when it happened on LinkedIn.
    detected_at: str | None = None
    post: SearchPostResult | None = None
    post_url: str | None = None
    comment: SignalComment | None = None
    reaction: SignalReaction | None = None
    viewer: ProfileViewer | None = None
    person_urn: str | None = None
    person_url: str | None = None
