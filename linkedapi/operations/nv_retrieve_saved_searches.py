from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import NvRetrieveSavedSearchesParams, NvSavedSearch


class NvRetrieveSavedSearches(Operation[NvRetrieveSavedSearchesParams, list[NvSavedSearch]]):
    """Retrieve owned saved searches of the requested type."""

    operation_name = "nvRetrieveSavedSearches"
    mapper = ArrayWorkflowMapper[NvRetrieveSavedSearchesParams, NvSavedSearch](
        "nv.retrieveSavedSearches", NvSavedSearch
    )
