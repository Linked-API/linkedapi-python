from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import NvCreatedList, NvCreateListParams


class NvCreateList(Operation[NvCreateListParams, NvCreatedList]):
    """Create an owned list, returning its string ID, stored name, type and URL.

    Name is trimmed (1-75 characters). Description has surrounding spaces trimmed, at most
    350 characters after trimming, and is omitted when blank. Same-type names
    equal after trimming, case-sensitive, including system lists, return listAlreadyExists.
    """

    operation_name = "nvCreateList"
    mapper = SimpleWorkflowMapper[NvCreateListParams, NvCreatedList](
        "nv.createList", result_model=NvCreatedList
    )
