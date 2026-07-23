from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import ReactToCommentParams


class ReactToComment(Operation[ReactToCommentParams, None]):
    """React to a LinkedIn comment."""

    operation_name = "reactToComment"
    mapper = VoidWorkflowMapper[ReactToCommentParams]("st.reactToComment")
