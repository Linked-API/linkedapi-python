from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ActionConfig, ResponseMapping, ThenWorkflowMapper
from linkedapi.types import FetchPostParams, Post


class FetchPostMapper(ThenWorkflowMapper[FetchPostParams, Post]):
    def __init__(self) -> None:
        super().__init__(
            action_configs=[
                ActionConfig(
                    "retrieve_comments", "st.retrievePostComments", "comments_retrieval_config"
                ),
                ActionConfig(
                    "retrieve_reactions", "st.retrievePostReactions", "reactions_retrieval_config"
                ),
            ],
            response_mappings=[
                ResponseMapping("st.retrievePostComments", "comments"),
                ResponseMapping("st.retrievePostReactions", "reactions"),
            ],
            base_action_type="st.openPost",
            default_params={"basicInfo": True},
            result_model=Post,
        )


class FetchPost(Operation[FetchPostParams, Post]):
    """Fetch a LinkedIn post."""

    operation_name = "fetchPost"
    mapper = FetchPostMapper()
