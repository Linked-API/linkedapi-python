from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import CreateRepostParams, CreateRepostResult


class CreateRepost(Operation[CreateRepostParams, CreateRepostResult]):
    """Repost a LinkedIn post, either as is or with your own commentary."""

    operation_name = "createRepost"
    mapper = SimpleWorkflowMapper[CreateRepostParams, CreateRepostResult](
        "st.createRepost",
        result_model=CreateRepostResult,
    )
