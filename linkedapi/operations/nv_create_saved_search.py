from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import SimpleWorkflowMapper
from linkedapi.types import NvCreatedSavedSearch, NvCreateSavedSearchParams


class NvCreateSavedSearch(Operation[NvCreateSavedSearchParams, NvCreatedSavedSearch]):
    """Save a Sales Navigator search URL matching the requested type. Returns its id, name,
    type and URL. English interface only.
    """

    operation_name = "nvCreateSavedSearch"
    mapper = SimpleWorkflowMapper[NvCreateSavedSearchParams, NvCreatedSavedSearch](
        "nv.createSavedSearch", result_model=NvCreatedSavedSearch
    )
