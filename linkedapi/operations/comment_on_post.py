from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import CommentOnPostParams


class CommentOnPost(Operation[CommentOnPostParams, None]):
    """Comment on a LinkedIn post."""

    operation_name = "commentOnPost"
    mapper = VoidWorkflowMapper[CommentOnPostParams]("st.commentOnPost")
