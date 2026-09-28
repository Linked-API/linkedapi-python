from __future__ import annotations

from typing import Literal, TypeAlias

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams

PostType = Literal["original", "repost"]
PostActorType = Literal["person", "company"]
ReactionType = Literal["like", "celebrate", "support", "love", "insightful", "funny"]
PostCommenterType = Literal["person", "company"]
PostEngagerType = Literal["person", "company"]
PostCommentsSort = Literal["mostRelevant", "mostRecent"]
AttachmentType = Literal["image", "video", "document"]


class Reaction(LinkedApiModel):
    post_url: str | None = None
    time: str | None = None
    reaction_type: ReactionType | None = None


class Comment(LinkedApiModel):
    post_url: str | None = None
    time: str | None = None
    text: str | None = None
    image: str | None = None
    reactions_count: int | None = None


class PostTargetParams(BaseActionParams):
    """A post is addressed by its URL or by its URN.

    Provide one of the two; when both are given, they must refer to the same post.
    """

    post_url: str | None = None
    post_urn: str | None = None


class ReactToPostParams(PostTargetParams):
    type: ReactionType
    company_url: str | None = None


class CommentOnPostParams(PostTargetParams):
    text: str
    company_url: str | None = None


class CommentResult(LinkedApiModel):
    comment_urn: str | None = None
    comment_url: str | None = None


CommentOnPostResult: TypeAlias = CommentResult


class ReactToCommentParams(BaseActionParams):
    comment_url: str
    type: ReactionType = "like"


class ReplyToCommentParams(BaseActionParams):
    comment_url: str
    text: str


ReplyToCommentResult: TypeAlias = CommentResult


class PostComment(LinkedApiModel):
    comment_urn: str | None = None
    comment_url: str | None = None
    commenter_url: str | None = None
    commenter_name: str | None = None
    commenter_headline: str | None = None
    commenter_type: PostCommenterType | None = None
    time: str | None = None
    text: str | None = None
    image: str | None = None
    is_reply: bool | None = None
    reactions_count: int | None = None
    replies_count: int | None = None


class PostReaction(LinkedApiModel):
    engager_urn: str | None = None
    engager_url: str | None = None
    engager_name: str | None = None
    engager_headline: str | None = None
    engager_type: PostEngagerType | None = None
    type: ReactionType | None = None


class PostAuthor(LinkedApiModel):
    type: PostActorType | None = None
    name: str | None = None
    urn: str | None = None
    profile_url: str | None = None
    headline: str | None = None
    company_url: str | None = None


class PostReposter(LinkedApiModel):
    type: PostActorType | None = None
    name: str | None = None
    urn: str | None = None
    profile_url: str | None = None
    headline: str | None = None
    company_url: str | None = None


class Post(LinkedApiModel):
    url: str | None = None
    time: str | None = None
    type: PostType | None = None
    activity_urn: str | None = None
    author: PostAuthor | None = None
    reposter: PostReposter | None = None
    repost_text: str | None = None
    hashtags: list[str] | None = None
    mentions: list[str] | None = None
    external_links: list[str] | None = None
    text: str | None = None
    images: list[str] | None = None
    document_slides: list[str] | None = None
    has_video: bool | None = None
    video_thumbnail: str | None = None
    has_poll: bool | None = None
    reactions_count: int | None = None
    comments_count: int | None = None
    reposts_count: int | None = None
    comments: list[PostComment] | None = None
    reactions: list[PostReaction] | None = None


class PostCommentsRetrievalConfig(LimitParams):
    replies: bool | None = None
    sort: PostCommentsSort | None = None


PostReactionsRetrievalConfig: TypeAlias = LimitParams


class BaseFetchPostParams(PostTargetParams):
    retrieve_comments: bool | None = None
    retrieve_reactions: bool | None = None


class BaseFetchPostParamsWide(BaseFetchPostParams):
    retrieve_comments: Literal[True] = True
    retrieve_reactions: Literal[True] = True


class FetchPostParams(BaseFetchPostParams):
    comments_retrieval_config: PostCommentsRetrievalConfig | None = None
    reactions_retrieval_config: PostReactionsRetrievalConfig | None = None


FetchPostResult: TypeAlias = Post


class CreatePostAttachment(LinkedApiModel):
    url: str
    type: AttachmentType
    name: str | None = None


class PostMention(LinkedApiModel):
    """One person or company to mention, bound to a "@[key]" placeholder in the post text.

    "name" is always required because LinkedIn's composer accepts nothing but typed text. The
    optional identifier decides which of the offered namesakes is taken; with "name" alone the pick
    is whichever suggestion LinkedIn ranked first. Provide at most one identifier.
    """

    key: str
    name: str
    urn: str | None = None
    person_hashed_url: str | None = None
    company_hashed_url: str | None = None


class CreatePostParams(BaseActionParams):
    text: str
    mentions: list[PostMention] | None = None
    attachments: list[CreatePostAttachment] | None = None
    company_url: str | None = None


class PublishedPostResult(LinkedApiModel):
    """Identifiers of a post this account has just published."""

    post_url: str | None = None
    post_urn: str | None = None


CreatePostResult: TypeAlias = PublishedPostResult


class CreateRepostParams(PostTargetParams):
    """Without "text" the post is reposted as is; with "text" the commentary goes above it."""

    text: str | None = None
    mentions: list[PostMention] | None = None


CreateRepostResult: TypeAlias = PublishedPostResult
