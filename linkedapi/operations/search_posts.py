from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import SearchPostResult, SearchPostsParams


class SearchPosts(Operation[SearchPostsParams, list[SearchPostResult]]):
    """Search posts on standard LinkedIn."""

    operation_name = "searchPosts"
    mapper = ArrayWorkflowMapper[SearchPostsParams, SearchPostResult](
        "st.searchPosts",
        SearchPostResult,
    )
