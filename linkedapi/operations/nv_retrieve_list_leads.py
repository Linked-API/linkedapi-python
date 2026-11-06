from __future__ import annotations

from linkedapi.core import Operation
from linkedapi.mappers import ArrayWorkflowMapper
from linkedapi.types import NvListLead, NvRetrieveListLeadsParams


class NvRetrieveListLeads(Operation[NvRetrieveListLeadsParams, list[NvListLead]]):
    """Retrieve list leads from an owned Sales Navigator list."""

    operation_name = "nvRetrieveListLeads"
    mapper = ArrayWorkflowMapper[NvRetrieveListLeadsParams, NvListLead](
        "nv.retrieveListLeads", NvListLead
    )
