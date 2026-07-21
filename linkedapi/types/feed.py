from __future__ import annotations

from pydantic import Field

from linkedapi.types.params import LimitParams
from linkedapi.types.post import Post


class FeedPost(Post):
    feed_context: str | None = None


class RetrieveFeedParams(LimitParams):
    limit: int | None = Field(default=None, ge=1, le=100)
