from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import FeedPost, RetrieveFeedParams


class RetrieveFeed(Operation[RetrieveFeedParams, list[FeedPost]]):
    """Retrieve posts from the current account's LinkedIn home feed."""

    operation_name = "retrieveFeed"
    mapper = ArrayWorkflowMapper[RetrieveFeedParams, FeedPost](
        "st.retrieveFeed",
        FeedPost,
    )
