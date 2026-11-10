from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import NvCreatedList, NvRenameListParams


class NvRenameList(Operation[NvRenameListParams, NvCreatedList]):
    """Rename an owned custom list. Trimmed name: 1-75 characters, no line breaks. Same name
    succeeds; duplicates return listAlreadyExists and system lists return listNotRenamable.
    """

    operation_name = "nvRenameList"
    mapper = SimpleWorkflowMapper[NvRenameListParams, NvCreatedList](
        "nv.renameList", result_model=NvCreatedList
    )
