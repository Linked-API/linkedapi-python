from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import CommentOnPostParams, CommentResult


class CommentOnPost(Operation[CommentOnPostParams, CommentResult]):
    """Comment on a LinkedIn post."""

    operation_name = "commentOnPost"
    mapper = SimpleWorkflowMapper[CommentOnPostParams, CommentResult](
        "st.commentOnPost",
        result_model=CommentResult,
    )
