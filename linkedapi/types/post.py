from __future__ import annotations

from typing import Literal, TypeAlias

from linkedapi.types.base import LinkedApiModel
from linkedapi.types.params import BaseActionParams, LimitParams

PostType = Literal["original", "repost"]
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


class ReactToPostParams(BaseActionParams):
    post_url: str
    type: ReactionType
    company_url: str | None = None


class CommentOnPostParams(BaseActionParams):
    post_url: str
    text: str
    company_url: str | None = None


class PostComment(LinkedApiModel):
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
    engager_url: str | None = None
    engager_name: str | None = None
    engager_headline: str | None = None
    engager_type: PostEngagerType | None = None
    type: ReactionType | None = None


class Post(LinkedApiModel):
    url: str | None = None
    time: str | None = None
    type: PostType | None = None
    repost_text: str | None = None
    text: str | None = None
    images: list[str] | None = None
    has_video: bool | None = None
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


class BaseFetchPostParams(BaseActionParams):
    post_url: str
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


class CreatePostParams(BaseActionParams):
    text: str
    attachments: list[CreatePostAttachment] | None = None
    company_url: str | None = None


class CreatePostResult(LinkedApiModel):
    post_url: str | None = None
