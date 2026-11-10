from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvDeleteSavedSearchParams


class NvDeleteSavedSearch(Operation[NvDeleteSavedSearchParams, None]):
    """Delete an owned saved search by its string ID. An absent search returns
    savedSearchNotFound.
    """

    operation_name = "nvDeleteSavedSearch"
    mapper = VoidWorkflowMapper[NvDeleteSavedSearchParams]("nv.deleteSavedSearch")
