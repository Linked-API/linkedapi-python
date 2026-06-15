from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import ReactToPostParams


class ReactToPost(Operation[ReactToPostParams, None]):
    """React to a LinkedIn post."""

    operation_name = "reactToPost"
    mapper = VoidWorkflowMapper[ReactToPostParams]("st.reactToPost")
