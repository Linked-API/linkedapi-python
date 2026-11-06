from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import NvList, NvRetrieveListsParams


class NvRetrieveLists(Operation[NvRetrieveListsParams, list[NvList]]):
    """Retrieve owned lists, preserving string IDs, upstream sources, and nullable counts."""

    operation_name = "nvRetrieveLists"
    mapper = ArrayWorkflowMapper[NvRetrieveListsParams, NvList]("nv.retrieveLists", NvList)
