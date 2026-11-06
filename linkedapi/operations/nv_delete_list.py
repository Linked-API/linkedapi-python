from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import VoidWorkflowMapper
from linkedapi.types import NvDeleteListParams


class NvDeleteList(Operation[NvDeleteListParams, None]):
    """Delete one owned list by string ID, keeping members saved and in their other lists.

    Unknown, shared or already-deleted lists return listNotFound. System lists without a
    Delete action return listNotDeletable. Success has no result data.
    """

    operation_name = "nvDeleteList"
    mapper = VoidWorkflowMapper[NvDeleteListParams]("nv.deleteList")
