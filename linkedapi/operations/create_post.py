from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import CreatePostParams, CreatePostResult


class CreatePost(Operation[CreatePostParams, CreatePostResult]):
    """Create a LinkedIn post."""

    operation_name = "createPost"
    mapper = SimpleWorkflowMapper[CreatePostParams, CreatePostResult](
        "st.createPost",
        result_model=CreatePostResult,
    )
