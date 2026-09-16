from __future__ import annotations

from typing import Literal, TypeAlias

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams
from linkedapi.types.post import PostActorType, PostType

PostSearchSort = Literal["topMatch", "latest"]
PostSearchDatePosted = Literal["past24Hours", "pastWeek", "pastMonth"]
PostSearchContentType = Literal["videos", "images", "jobPosts", "liveVideos", "documents"]
PostSearchPostedBy = Literal["me", "firstConnections", "peopleYouFollow"]


class SearchPostsPersonFilter(LinkedApiModel):
    """One person to narrow a post search by.

    "name" is always required because LinkedIn's filter panel accepts nothing but typed text. The
    optional identifier decides which of the offered namesakes is taken; with "name" alone the pick
    is whichever suggestion LinkedIn ranked first.
    """

    name: str
    urn: str | None = None
    person_hashed_url: str | None = None


class SearchPostsCompanyFilter(LinkedApiModel):
    """One company to narrow a post search by. Same contract as SearchPostsPersonFilter."""

    name: str
    urn: str | None = None
    company_hashed_url: str | None = None


# A plain string is shorthand for the name alone: "Bill Gates" means {"name": "Bill Gates"}.
# Both forms may be mixed in one list.
SearchPostsPersonFilterEntry: TypeAlias = SearchPostsPersonFilter | str
SearchPostsCompanyFilterEntry: TypeAlias = SearchPostsCompanyFilter | str


class SearchPostsFilter(LinkedApiModel):
    """Filtering criteria for the LinkedIn content search.

    Every specified field is applied, or the action fails. Ignored entirely when
    "custom_search_url" is specified.
    """

    sort: PostSearchSort | None = None
    date_posted: PostSearchDatePosted | None = None
    content_type: PostSearchContentType | None = None
    posted_by: list[PostSearchPostedBy] | None = None
    from_members: list[SearchPostsPersonFilterEntry] | None = None
    from_companies: list[SearchPostsCompanyFilterEntry] | None = None
    mentioning_members: list[SearchPostsPersonFilterEntry] | None = None
    mentioning_companies: list[SearchPostsCompanyFilterEntry] | None = None
    author_companies: list[SearchPostsCompanyFilterEntry] | None = None
    author_industries: list[str] | None = None


class SearchPostsParams(BaseActionParams, LimitParams):
    # Either "term" or "custom_search_url" must be provided. "limit" defaults to 10 and may go up
    # to 100, or up to 20 when child actions are attached.
    term: str | None = None
    filter: SearchPostsFilter | None = None
    custom_search_url: str | None = None


class SearchPostActor(LinkedApiModel):
    """Whoever a search result attributes content to: its author, or the actor that reshared it.

    Unlike the actors of a post returned by fetch_post, these carry no "urn": the URN is read from
    identity anchors on the post's own page, and a search result list has none of them.
    """

    type: PostActorType | None = None
    name: str | None = None
    profile_url: str | None = None
    headline: str | None = None
    company_url: str | None = None


class SearchPostResult(LinkedApiModel):
    url: str | None = None
    activity_urn: str | None = None
    time: str | None = None
    type: PostType | None = None
    author: SearchPostActor | None = None
    # Non-null only when "type" is "repost".
    reposter: SearchPostActor | None = None
    text: str | None = None
    repost_text: str | None = None
    hashtags: list[str] | None = None
    mentions: list[str] | None = None
    external_links: list[str] | None = None
    images: list[str] | None = None
    document_slides: list[str] | None = None
    has_video: bool | None = None
    video_thumbnail: str | None = None
    has_poll: bool | None = None
    reactions_count: int | None = None
    comments_count: int | None = None
    reposts_count: int | None = None
