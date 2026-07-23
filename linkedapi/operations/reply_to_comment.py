from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import CommentResult, ReplyToCommentParams


class ReplyToComment(Operation[ReplyToCommentParams, CommentResult]):
    """Reply to a LinkedIn comment."""

    operation_name = "replyToComment"
    mapper = SimpleWorkflowMapper[ReplyToCommentParams, CommentResult](
        "st.replyToComment",
        result_model=CommentResult,
    )
